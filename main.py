from os import path
import configparser
from PIL import Image, ImageDraw, ImageFont
from display import DisplayDriver
from reader.epub_render import TextRenderer

from time import sleep

BOOK_DIR: str = path.join(path.dirname(__file__), "Books")


if __name__ == "__main__":
    print("Hello world!")
    display: DisplayDriver = DisplayDriver(480, 800, 90)
    display.initialize()
    display.clear()

    font24 = ImageFont.truetype(path.join("/usr/share/fonts/truetype/dejavu/", 'DejaVuSans-Bold.ttf'), 24)
    font18 = ImageFont.truetype(path.join("/usr/share/fonts/truetype/dejavu/", 'DejaVuSans-Bold.ttf'), 18)
    font35 = ImageFont.truetype(path.join("/usr/share/fonts/truetype/dejavu/", 'DejaVuSans-Bold.ttf'), 35)
    Himage = Image.new('1', (480, 800), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'Doodler', font = font35, fill = 0)
    draw.line((10, 20, 470, 20), fill = 0)
    display.display_image(Himage)

    # epub_path = path.join(BOOK_DIR, "moby-dick.epub")
    # renderer = TextRenderer(epub_path, 480, 800)
    # pg7: Image.Image = renderer.render_page(25)

    # Himage = Image.open(path.join(BOOK_DIR, "7in5_V2.bmp"))
    # display.initialize()
    # display.clear()
    # # display.display(display.epd.getbuffer(Himage))
    # display.display_image(pg7)
    sleep(10)
    display.clear()
    
    # pg7.save(path.join(BOOK_DIR, "page7.png"))

    # https://pymupdf.readthedocs.io/en/latest/recipes-text.html#recipestext