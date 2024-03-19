import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 630
ENABLE_DESCRIPTION = False
os.makedirs("output", exist_ok=True)


def wrap_text(text: str, font: ImageFont, max_width: int, lang: str = "en") -> list:
    """
    Wrap text box to fit the width limits
    :param text: Full text to be wrapped
    :param font: ImageFont object so that we can get the size of the text
    :param max_width: Maximum width of the text box
    :param lang: Based on the language, split the text differently
    :return: list of lines
    """
    lines = []
    if lang == "en":
        words = text.split()
        current_line = words[0]
    else:
        words = list(text)
        current_line = words[0]
    for word in words[1:]:
        if font.font.getsize(current_line)[0][0] <= max_width:
            if lang == "en":
                current_line += ' ' + word
            else:
                current_line += word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines


def make_open_graph_image_with_description(title: str, description: str, hash_key: str, lang: str = "en"):
    if lang == "en":
        HEADER = "Snap Hutao Official Website"
    else:
        HEADER = "Snap Hutao 官方网站"

    if lang == "en":
        footer = "Snap Hutao: Multifunctional Open-source Genshin Impact Toolkit"
    else:
        footer = "胡桃工具箱： 实用的开源多功能原神工具箱"

    # create canvas
    canvas = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT))

    # add background image
    bg_image = Image.open('src/bg.png')
    canvas.paste(bg_image, (0, 0))

    # create font object
    if lang == "en":
        title_font = ImageFont.truetype('src/genshin.ttf', 50)
    else:
        title_font = ImageFont.truetype('src/genshin.ttf', 100)
    description_font = ImageFont.truetype('src/genshin.ttf', 30)
    footer_font = ImageFont.truetype('src/genshin.ttf', 25)

    # create draw object and text box
    draw = ImageDraw.Draw(canvas)

    header_position = (60, 110)
    title_position = (50, 150)
    description_position = (50, 300)
    footer_position = (50, 540)
    logo_position = (820, 150)
    footer_img_position = (710, 520)

    # add auto-next-line text box
    title_lines = wrap_text(title, title_font, 800, lang)
    description_lines = wrap_text(description, description_font, 580, lang)
    footer_lines = wrap_text(footer, footer_font, 500, lang)

    # draw Header
    draw.text(header_position, HEADER, font=footer_font, fill='#eb5b52')

    # draw title
    for i, line in enumerate(title_lines):
        line_position = (title_position[0], title_position[1] + i * title_font.font.getsize(title)[0][1])
        draw.text(line_position, line, font=title_font, fill='black')

    # draw description
    for i, line in enumerate(description_lines):
        line_position = (description_position[0], description_position[1] + i * description_font.font.
                         getsize(description)[0][1] * 1.1)
        draw.text(line_position, line, font=description_font, fill='black')

    # draw footer
    for i, line in enumerate(footer_lines):
        line_position = (footer_position[0], footer_position[1] + i * footer_font.font.getsize(footer)[0][1])
        draw.text(line_position, line, font=footer_font, fill='black')

    # add logo image
    logo_image = Image.open('src/logo.png')
    logo_image.convert("RGBA")
    logo_image = logo_image.resize((280, 280))
    canvas.paste(logo_image, logo_position, mask=logo_image)

    # add footer image
    if lang == "en":
        footer_image = Image.open('src/en-footer.png')
    else:
        footer_image = Image.open('src/chs-footer.png')
    footer_image.convert("RGBA")
    if lang == "en":
        footer_image = footer_image.resize((420, 55))
    else:
        footer_image = footer_image.resize((400, 55))
    canvas.paste(footer_image, footer_img_position, mask=footer_image)

    # export image
    output_file = f"./output/{hash_key}.png"
    canvas.save(output_file)

    return True


def make_open_graph_image_with_no_description(title: str, hash_key: str, lang: str = "en"):
    if lang == "en":
        HEADER = "Snap Hutao Official Website"
    else:
        HEADER = "Snap Hutao 官方网站"

    if lang == "en":
        footer = "Snap Hutao: Multifunctional Open-source Genshin Impact Toolkit"
    else:
        footer = "胡桃工具箱： 实用的开源多功能原神工具箱"

    # create canvas
    canvas = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT))

    # add background image
    bg_image = Image.open('src/bg.png')
    canvas.paste(bg_image, (0, 0))
    # create font object
    if lang == "en":
        title_font = ImageFont.truetype('src/genshin.ttf', 55)
        footer_font = ImageFont.truetype('src/genshin.ttf', 35)
    else:
        if len(title) > 5:
            title_font = ImageFont.truetype('src/genshin.ttf', 80)
        else:
            title_font = ImageFont.truetype('src/genshin.ttf', 110)
        footer_font = ImageFont.truetype('src/genshin.ttf', 45)

    # create draw object and text box
    draw = ImageDraw.Draw(canvas)

    header_position = (60, 110)
    title_position = (50, 180)
    footer_position = (50, 420)
    logo_position = (820, 150)
    footer_img_position = (610, 520)

    # add auto-next-line text box
    title_lines = wrap_text(title, title_font, 550, lang)
    footer_lines = wrap_text(footer, footer_font, 500, lang)

    # draw Header
    draw.text(header_position, HEADER, font=footer_font, fill='#eb5b52')

    # draw title
    for i, line in enumerate(title_lines):
        line_position = (title_position[0], title_position[1] + i * title_font.font.getsize(title)[0][1] * 1.2)
        draw.text(line_position, line, font=title_font, fill='black')

    # draw footer
    for i, line in enumerate(footer_lines):
        line_position = (footer_position[0], footer_position[1] + i * footer_font.font.getsize(footer)[0][1] * 1.2)
        draw.text(line_position, line, font=footer_font, fill='black')

    # add logo image
    logo_image = Image.open('src/logo.png')
    logo_image.convert("RGBA")
    logo_image = logo_image.resize((280, 280))
    canvas.paste(logo_image, logo_position, mask=logo_image)

    # add footer image
    if lang == "en":
        footer_image = Image.open('src/en-footer.png')
    else:
        footer_image = Image.open('src/chs-footer.png')
    footer_image.convert("RGBA")
    if lang == "en":
        footer_image = footer_image.resize((500, 65))
    else:
        footer_image = footer_image.resize((500, 70))
    canvas.paste(footer_image, footer_img_position, mask=footer_image)

    # export image
    output_file = f"./output/{hash_key}.png"
    canvas.save(output_file)

    return True


def hutao_docs_parser(url: str, hash_key: str, lang: str = "en"):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    this_title = soup.find("meta", {"property": "og:title"})["content"]
    this_description = soup.find("meta", {"property": "og:description"})["content"]
    if hash_key.endswith("1"):
        make_open_graph_image_with_description(this_title, this_description, hash_key, lang)
    else:
        make_open_graph_image_with_no_description(this_title, hash_key, lang)
    return True


if __name__ == "__main__":
    hutao_docs_parser("https://hut.ao/zh/features/mhy-account-switch.html", hash_key="test", lang="zh")
    hutao_docs_parser("https://hut.ao/en/features/mhy-account-switch.html", hash_key="test2", lang="en")