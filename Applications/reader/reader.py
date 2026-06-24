# from display import DisplayDriver



# class Reader:
#     def __init__(self, display:DisplayDriver):
#         pass

import io
from pathlib import Path

import ebooklib
from ebooklib import epub

if __name__ == "__main__":
    book = epub.read_epub("C:\\Users\\gkorthuis\\source\\Doodler\\Books\\hf.epub")

    print(book.get_metadata('DC', 'title'))
    book.get_metadata('OPF', 'cover')
    item = book.toc[0]

    x = 0
    
    