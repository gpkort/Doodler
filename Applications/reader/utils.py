from dataclasses import dataclass, field
from PIL import Image
from os import path
import sqlite3
import json
from ebooklib.epub import EpubBook

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
    current_page: int = 0
    pages: list = field(default_factory=list)  # List of pages, each page is a list of render items (text or image)
    page_count: int = 0
    images: dict[str, Image.Image] = field(default_factory=dict)  # Cache for EPUB images: {src_path: PIL.Image}
    custom_fonts: dict[str, str] = field(default_factory=dict) # Cache for EPUB embedded fonts: {font_name: font_path}
    book: EpubBook | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "epub_path": self.epub_path,
            "cache_path": self.cache_path,
            "current_page": self.current_page,

            "pages": self.pages,
            "page_count": self.page_count,
            "images": {k: v for k, v in self.images.items()} if self.images else None,
            "custom_fonts": self.custom_fonts,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

def get_library_books() -> list[Book]:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT BookID, title, author, epub, cache, current_page FROM Books")
    rows = cursor.fetchall()
    conn.close()

    books = [Book(id=row[0], title=row[1], author=row[2], epub_path=row[3], cache_path=row[4], current_page=row[5]) for row in rows]
    return books





