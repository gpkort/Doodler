import sys
from pathlib import Path
from ebooklib.epub import EpubBook
import tkinter as tk
from PIL import Image

parent_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(parent_dir))

from epub_render import TextRenderer
from utils import Book
from display import SCREEN_HEIGHT, SCREEN_WIDTH
from input import  TkButtonInputHandler
from display import TkDisplayDriver
from input import  EventHandler, Event


# C:\Users\gkorthuis\source\Doodler\Books
BOOK_PATH = Path("Books/hf.epub").resolve()
BOOK_SHELF = Path("BookShelf").resolve()
HUCK_FINN = Book(0, "Huckleberry Finn", "Mark Twain", str(BOOK_PATH), str(BOOK_SHELF))

root = tk.Tk()
root.title("Doodler")
display = TkDisplayDriver(root)
tr = TextRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
event_dispatcher = TkButtonInputHandler(root)
current:int = 25

def right(data: dict):
    global current, tr
    current = (current + 1) if current < HUCK_FINN.page_count else 0
    print(f"Right: {current}, info: {HUCK_FINN.pages[25]}")
    img: Image.Image = tr.render_page(25) 
    if img:
        display.display_image(img)
    
def left(data: dict):
    global current, tr
    current = (current - 1) if current > 0 else 0
    print(f"Left: {current}, info: {HUCK_FINN.pages[25]}")
    img: Image.Image = tr.render_page(25) 
    if img:
        display.display_image(img)
    print("Done")

event_dispatcher.register_handler(EventHandler(Event.LEFT, left))
event_dispatcher.register_handler(EventHandler(Event.RIGHT, right))
tr.load_epub(HUCK_FINN)



if __name__ == "__main__":
            
    tr.render_page(50)
    
    
    root.mainloop()

    print("Cool")
