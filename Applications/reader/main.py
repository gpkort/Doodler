import sys
from pathlib import Path
from ebooklib.epub import EpubBook
import tkinter as tk
from PIL import Image

parent_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(parent_dir))

from utils import Book
from display import SCREEN_HEIGHT, SCREEN_WIDTH
from input import  TkButtonInputHandler
from display import TkDisplayDriver
from input import  EventHandler, Event

from epub_render import PillowTextRenderer


# C:\Users\gkorthuis\source\Doodler\Books
BOOK_PATH = Path("Books/hf.epub").resolve()
BOOK_SHELF = Path("BookShelf").resolve()
HUCK_FINN = Book(0, "Huckleberry Finn", "Mark Twain", str(BOOK_PATH), str(BOOK_SHELF))

root = tk.Tk()
root.title("Doodler")
display = TkDisplayDriver(root)
event_dispatcher = TkButtonInputHandler(root)
current:int = 7
page_count = 0;

def right(data: dict):
    global current, ptr
    current = (current + 1) if current < page_count else 0
    print(f"Right: {current}, {page_count}")
    img: Image.Image = ptr.render_page(current) 
    if img:
        display.display_image(img)
    
def left(data: dict):
    global current, ptr
    current = (current - 1) if current > 0 else 0
    print(f"Left: {current}, {page_count}")
    img: Image.Image = ptr.render_page(current) 
    if img:
        display.display_image(img)
    print("Done")

event_dispatcher.register_handler(EventHandler(Event.LEFT, left))
event_dispatcher.register_handler(EventHandler(Event.RIGHT, right))

if __name__ == "__main__":
            
    ptr:PillowTextRenderer = PillowTextRenderer("C:\\Users\\gkorthuis\\source\\Doodler\\Books\\hf.epub", SCREEN_WIDTH, SCREEN_HEIGHT)
    page_count = ptr.get_page_count()
    print(f"main: total {page_count}, page {current}")
    img: Image.Image = ptr.render_page(current)
    display.display_image(img)

    print("Cool")
    
    
    root.mainloop()
    
