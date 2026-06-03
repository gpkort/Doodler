from dataclasses import dataclass
from os import path
import sqlite3

DATABASE_PATH = "data/media.sqlite3"
THUMBNAIL_PATH = "Books/thumbnails/"
LIBRARY_PATH = "Books/library/"
BOOK_SHELF_PATH = "Books/shelf/"


@dataclass
class Book:
    id: int
    title: str
    author: str
    epub_path: str
    cache_path: str

def get_library_books() -> list[Book]:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT BookID, title, epub, thumbnail FROM Books")
    rows = cursor.fetchall()
    conn.close()
    
    books = [Book(id=row[0], title=row[1], author=row[2], epub_path=row[3], cache_path=row[4]) for row in rows]
    return books





