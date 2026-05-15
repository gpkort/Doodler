from os import path
import configparser



from PIL import Image, ImageDraw, ImageFont

from reader.epub_render import TextRenderer

BOOK_DIR: str = path.join(path.dirname(__file__), "Books")


if __name__ == "__main__":
    print("Hello world!")
    # epub_path = path.join(BOOK_DIR, "moby-dick.epub")
    # renderer = TextRenderer(epub_path)
    # print(f"page count: {renderer.page_count}")
    # pg7: Image.Image = renderer.render_page(25)
    # pg7.save(path.join(BOOK_DIR, "page7.png"))
    # print("Hello world!")

    # https://pymupdf.readthedocs.io/en/latest/recipes-text.html#recipestext