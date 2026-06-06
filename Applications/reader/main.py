import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(parent_dir))

from epub_render import TextRenderer
from utils import Book
from display import DisplayDriver, SCREEN_HEIGHT, SCREEN_WIDTH
from UI import AppController

# C:\Users\gkorthuis\source\Doodler\Books
BOOK_PATH = Path("Books/hf.epub").resolve()
BOOK_SHELF = Path("BookShelf").resolve()

HUCK_FINN = Book(0, "Huckleberry Finn", "Mark Twain", str(BOOK_PATH), "./")

if __name__ == "__main__":
    tr = TextRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    print(BOOK_PATH)
    print(BOOK_SHELF)
    tr.load_epub(HUCK_FINN)

    print("Cool")
