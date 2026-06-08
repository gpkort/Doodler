import sys
from pathlib import Path
from PIL import Image

parent_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(parent_dir))

from epub_render import TextRenderer
from utils import Book
from display import SCREEN_HEIGHT, SCREEN_WIDTH
from input import  TkButtonInputHandler
from display import TkDisplayDriver
from input import  EventHandler, Event

class PageManager:
    def __init__(self):
        pass