import io
# from pathlib import Path
from os import path

import ebooklib
from ebooklib import epub

BOOK_PATH = "C:\\repos\\Doodler\\Books"
BOOK_NAME = "hf.epub"

if __name__ == "__main__":
    book = epub.read_epub(path.join(BOOK_PATH, BOOK_NAME))
    print(len(book.pages))
    x = 0