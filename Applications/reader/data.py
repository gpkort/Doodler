from dataclasses import dataclass
from os import path
import sqlite3

DATABASE_PATH = "data/media.sqlite3"
THUMBNAIL_PATH = "Books/thumbnails/"
LIBRARY_PATH = "Books/library/"
BOOK_SHELF_PATH = "Books/shelf/"

@dataclass
class BookshelfItem:
    title: str
    author: str
    path: str
    cover: Image.Image

@dataclass
class Book:
    id: int
    title: str
    epub_path: str

def get_library_books() -> list[Book]:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT BookID, title, epub, thumbnail FROM Books")
    rows = cursor.fetchall()
    conn.close()
    
    books = [Book(id=row[0], title=row[1], epub_path=row[2]) for row in rows]
    return books





