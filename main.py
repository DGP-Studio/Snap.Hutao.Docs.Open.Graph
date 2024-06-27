import uvicorn
import os
import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from urllib.parse import urlparse
from open_graph import hutao_docs_parser, fuck_gitcode_png
from server_config import API_VERSION, SERVER_DESCRIPTION, CONTACT_INFO, LICENSE_INFO

app = FastAPI(redoc_url=None,
              title="Snap Hutao Open Graph Image Server",
              summary="Open Graph image server.",
              version=API_VERSION,
              description=SERVER_DESCRIPTION,
              contact=CONTACT_INFO,
              license_info=LICENSE_INFO,
              openapi_url="/openapi.json")


@app.get("/")
async def root():
    return {"message": "Hello, Open Graph!"}


@app.get("/generate")
async def generate_open_graph_image(url: str, has_description: bool = False):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ["http", "https"]:
        raise HTTPException(status_code=400, detail="Invalid URL scheme")
    if parsed_url.hostname not in ["hut.ao", "deploy-preview-117--snap-hutao-docs.netlify.app"]:
        print(f"Invalid hostname: {parsed_url.hostname}")
        raise HTTPException(status_code=400, detail="Invalid hostname")
    uri = parsed_url.path
    if "/zh/" in uri:
        lang = "zh"
    else:
        lang = "en"
    hashed_uri = hashlib.md5(uri.encode()).hexdigest()
    if has_description:
        hashed_uri = hashed_uri + "1"
    else:
        hashed_uri = hashed_uri + "0"

    # check if the image exists, if exist return the image
    if os.path.exists(f"output/{hashed_uri}.png"):
        return FileResponse(f"output/{hashed_uri}.png")
    else:
        result = hutao_docs_parser(url, hashed_uri, lang)
        if result:
            return FileResponse(f"output/{hashed_uri}.png")
        else:
            raise HTTPException(status_code=500, detail="Failed to generate Open Graph image")


@app.get("/gitcode")
async def generate_gitcode_image(repo: str):
    org_name, repo_name = repo.split("/")
    if os.path.exists(f"output/gitcode/{org_name}/{repo_name}.png"):
        print("cached")
        return FileResponse(f"output/gitcode/{org_name}/{repo_name}.png")
    else:
        if fuck_gitcode_png(org_name, repo_name):
            print("created")
            return FileResponse(f"output/gitcode/{org_name}/{repo_name}.png")
        else:
            return FileResponse(f"src/gitcode/pixel.png")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, proxy_headers=True, forwarded_allow_ips="*")
