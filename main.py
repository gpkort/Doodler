from os import path
import platform
import configparser
import logging
from typing import Any
import tkinter as tk

from input import  KeyboardInputHandler, TkButtonInputHandler
from PIL import ImageFont, Image

import UI
# from PIL import Image, ImageDraw, ImageFont
from display import TkDisplayDriver, DisplayDriver, fontmanager, FontConfig, FontSize, make_icons
# from reader.epub_render import TextRenderer

#Add some comments

BOOK_DIR: str = path.join(path.dirname(__file__), "Books")
CONFIG_FILE_NAME: str = "config.ini"

config: configparser.ConfigParser | None = None
display_settings: dict[str, Any] | None = None
quitting: bool = False

def load_config(config_file_name: str = CONFIG_FILE_NAME) -> configparser.ConfigParser:
    ret = configparser.ConfigParser()
    file = ret.read(path.join(path.dirname(__file__), config_file_name))

    if(not file):
        raise FileNotFoundError(f"Config file {config_file_name} not found in {path.dirname(__file__)}")
    return ret

def setup_logging(config_parse: configparser.ConfigParser):
    log_level = config_parse.get("System", "log_level", fallback="INFO")
    log_file = config_parse.get("System", "log_file", fallback="doodler.log")
    logging.basicConfig(level=log_level, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')

def get_display_settings(config_parse: configparser.ConfigParser) -> dict[str, Any]:
    width = config_parse.getint("Display", "width", fallback=480)
    height = config_parse.getint("Display", "height", fallback=800)
    orientation = config_parse.getint("Display", "orientation", fallback=90)
    use_local_display = config_parse.getboolean("Display", "use_local_display", fallback=True)
    return {"width": width, "height": height, "orientation": orientation, "use_local_display": use_local_display}

def get_font_settings(config_parse: configparser.ConfigParser) -> list[FontConfig]:
    font_path:str
    font_name:str
    if platform.system() == "Windows":
        font_path = config_parse.get("Fonts", "windows_font_path", fallback="C:\\Windows\\Fonts\\")
        font_name = config_parse.get("Fonts", "windows_font_name", fallback="Arial.ttf")
    else:
        font_path = config_parse.get("Fonts", "linux_font_path", fallback="/usr/share/fonts/truetype/dejavu/")
        font_name = config_parse.get("Fonts", "linux_font_name", fallback="DejaVuSans.ttf")

    small_font_size = config_parse.getint("Fonts", "small_font_size", fallback=18)
    medium_font_size = config_parse.getint("Fonts", "medium_font_size", fallback=24)
    large_font_size = config_parse.getint("Fonts", "large_font_size", fallback=36)
    
    return [
        FontConfig(path=font_path, name=font_name, font_size=FontSize.SMALL, actual_size=small_font_size),
        FontConfig(path=font_path, name=font_name, font_size=FontSize.MEDIUM, actual_size=medium_font_size),
        FontConfig(path=font_path, name=font_name, font_size=FontSize.LARGE, actual_size=large_font_size)
    ]

def exit_program():
    global quitting
    logging.info("Exiting Doodler")
    quitting = True
    exit(0)
    
def main():
    global config, display_settings,quitting
    
    config = load_config()
    setup_logging(config)
    logging.info("Starting Doodler")
    display_settings = get_display_settings(config)
    font_settings = get_font_settings(config)
    fontmanager.initialize(font_settings)
    root = tk.Tk()
    root.title("Doodler")
    appManager: UI.AppManager = UI.AppManager(TkDisplayDriver(root), TkButtonInputHandler(root), exit_program)
    
    
    root.mainloop()
    print("Exited main loop, quitting:")
    
    while not quitting:
        ...
        
    exit(0)

if __name__ == "__main__":
    
    main()

    # display: DisplayDriver = DisplayDriver(480, 800, 90)
    # display.initialize()
    # display.clear()

    
   

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