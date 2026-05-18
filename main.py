from os import path
import configparser
import logging
from typing import Any

from UI import HomeScreen
# from PIL import Image, ImageDraw, ImageFont
from display import DisplayDriver
# from reader.epub_render import TextRenderer

from time import sleep

BOOK_DIR: str = path.join(path.dirname(__file__), "Books")
CONFIG_FILE_NAME: str = "config.ini"

config: configparser.ConfigParser = None
display_settings: dict[str, int] = None

def load_config(config_file_name: str = CONFIG_FILE_NAME) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    file = config.read(path.join(path.dirname(__file__), config_file_name))

    if(not file):
        raise FileNotFoundError(f"Config file {config_file_name} not found in {path.dirname(__file__)}")
    return config

def setup_logging(config: configparser.ConfigParser):
    log_level = config.get("System", "log_level", fallback="INFO")
    log_file = config.get("System", "log_file", fallback="doodler.log")
    logging.basicConfig(level=log_level, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')

def get_display_settings(config: configparser.ConfigParser) -> dict[str, Any]:
    width = config.getint("Display", "width", fallback=480)
    height = config.getint("Display", "height", fallback=800)
    orientation = config.getint("Display", "orientation", fallback=90)
    use_local_display = config.getboolean("Display", "use_local_display", fallback=True)
    return {"width": width, "height": height, "orientation": orientation}

def main():
    config = load_config()
    setup_logging(config)
    logging.info("Starting Doodler")
    display_settings = get_display_settings(config)



if __name__ == "__main__":
    main()
    home_screen = HomeScreen()

    # display: DisplayDriver = DisplayDriver(480, 800, 90)
    # display.initialize()
    # display.clear()

    # font24 = ImageFont.truetype(path.join("/usr/share/fonts/truetype/dejavu/", 'DejaVuSans-Bold.ttf'), 24)
    # font18 = ImageFont.truetype(path.join("/usr/share/fonts/truetype/dejavu/", 'DejaVuSans-Bold.ttf'), 18)
    # font35 = ImageFont.truetype(path.join("/usr/share/fonts/truetype/dejavu/", 'DejaVuSans-Bold.ttf'), 35)
    # Himage = Image.new('1', (480, 800), 255)
    # draw = ImageDraw.Draw(Himage)
    # draw.text((10, 0), 'Doodler', font = font35, fill = 0)
    # draw.line((10, 20, 470, 20), fill = 0)
    # display.display_image(Himage)

    # epub_path = path.join(BOOK_DIR, "moby-dick.epub")
    # renderer = TextRenderer(epub_path, 480, 800)
    # pg7: Image.Image = renderer.render_page(25)

    # Himage = Image.open(path.join(BOOK_DIR, "7in5_V2.bmp"))
    # display.initialize()
    # display.clear()
    # # display.display(display.epd.getbuffer(Himage))
    # display.display_image(pg7)
    # sleep(10)
    # display.clear()
    
    # pg7.save(path.join(BOOK_DIR, "page7.png"))

    # https://pymupdf.readthedocs.io/en/latest/recipes-text.html#recipestext