from os import path
import configparser
from PIL import Image, ImageDraw, ImageFont
from display.local_display import LocalDisplay
from reader.epub_render import TextRenderer

BOOK_DIR: str = path.join(path.dirname(__file__), "Books")


if __name__ == "__main__":
    print("Hello world!")
    local_display:LocalDisplay = LocalDisplay(480, 800)
    epub_path = path.join(BOOK_DIR, "moby-dick.epub")
    renderer = TextRenderer(epub_path, 480, 800)
    # print(f"page count: {renderer.page_count}")
    pg7: Image.Image = renderer.render_page(25)
    local_display.display(pg7.tobytes())
    # pg7.save(path.join(BOOK_DIR, "page7.png"))
    # print("Hello world!")

    # https://pymupdf.readthedocs.io/en/latest/recipes-text.html#recipestext