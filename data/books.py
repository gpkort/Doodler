from dataclasses import dataclass
from os import path
import sqlite3
# from data import DATABASE_PATH

DATABASE_PATH = "data/media.sqlite3"
THUMBNAIL_PATH = "Books/thumbnails/"

@dataclass
class Book:
    id: int
    title: str
    epub_path: str
    thumbnail_path: str

def get_books() -> list[Book]:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT BookID, title, epub, thumbnail FROM Books")
    rows = cursor.fetchall()
    conn.close()
    
    books = [Book(id=row[0], title=row[1], epub_path=row[2], thumbnail_path=path.join(THUMBNAIL_PATH, row[3])) for row in rows]
    return books





