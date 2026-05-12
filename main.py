from os import path

import ebooklib
from ebooklib import epub

if __name__ == "__main__":
    print("Hello world!")
    book: epub.EpubBook = epub.read_epub(path.join("Books", "moby-dick.epub"))
    book_items = list(book.get_items())

    # for bi in book_items:
    print(book_items[0].get_type() == ebooklib.ITEM_DOCUMENT)
    print(book_items[0].get_content())

    # print(book.get_metadata('DC', 'title'))
    # print(book.get_metadata('DC', 'creator'))
    # print(book.get_metadata('DC', 'identifier'))
    # for t in book.toc:
    #     print(f"t.href: {t.href}, t.title: {t.title}")