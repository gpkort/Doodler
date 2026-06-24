import sys
import re
from dataclasses import dataclass
from pathlib import Path
import os
import ebooklib
from ebooklib import epub
from PIL import Image, ImageDraw, ImageFont, ImageFile
from bs4 import BeautifulSoup,  Tag
from bs4.element import NavigableString

parent_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(parent_dir))

from display import SCREEN_HEIGHT, SCREEN_WIDTH

@dataclass
class TextToken:
    text: str
    style: str  # 'normal', 'bold', 'italic', 'bold_italic', 'h1', 'h2', 'center'
    new_paragraph: bool = False
    align: str = 'left'  # 'left', 'center', 'right'

@dataclass
class ImageToken:
    image: Image.Image
    max_width: int  # Maximum width in pixels
    max_height: int  # Maximum height in pixels
    new_paragraph: bool = True

@dataclass
class TableToken:
    rows: list[list[str]]  # 2D array of cell contents
    max_width: int  # Maximum width for table
    new_paragraph: bool = True

# BOOK_PATH = "C:\\repos\\Doodler\\Books"
BOOK_PATH = "C:\\Users\\gkorthuis\\source\\Doodler\\Books"
BOOK_NAME = "hf.epub"

# Optional: SVG support (requires cairosvg)
try:
    import cairosvg
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False
except OSError: 
    SVG_SUPPORT = False


def get_cover(book:epub.EpubBook)->Image.Image | None:
    # cover:epub.EpubCover = book.get_items_of_type(ebooklib.ITEM_COVER)
    # print file_name, id
    image:Image.Image | None = None
    cl = list(book.get_items_of_type(ebooklib.ITEM_COVER))
    if(len(cl) > 0):
        cover:epub.EpubCover = cl[0]
        image = convert_images(cover.get_name(), cover.get_content())

    return image

def convert_images(name:str, content:bytes) -> Image.Image | None:
    image: Image.Image | None = None

    try:
        # Check if this is an SVG file
        if name.lower().endswith('.svg'):
            if SVG_SUPPORT:
                try:
                    # Convert SVG to PNG using cairosvg
                    png_data = cairosvg.svg2png(bytestring=content, output_width=800) #type: ignore
                    image = Image.open(BytesIO(png_data)) #type: ignore
                except Exception as e:
                    print(f"Failed to convert SVG {name}: {e}")
        else:
            # Regular raster image (PNG, JPG, GIF, etc.)
            image = Image.open(BytesIO(content))  #type: ignore

            # Convert to appropriate mode for e-ink
            if image.mode == 'RGBA':      #type: ignore
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))    #type: ignore
                background.paste(image, mask=img.split()[3])  # Use alpha channel as mask  #type: ignore
                image = background
            elif image.mode not in ['RGB', 'L', '1']:  #type: ignore
                image = img.convert('RGB')     #type: ignore       
    except Exception as e:
        print(f"Failed to extract image {name}")

    return image

def get_embeded_fonts(book:epub.EpubBook) -> dict[str, str]:
    """Extract embedded fonts from EPUB"""
    import tempfile

    custom_fonts: dict[str, str] = {}

    for item in book.get_items():
        item_name = item.get_name().lower()
        if any(item_name.endswith(ext) for ext in ['.ttf', '.otf']):
            try:
                font_data = item.get_content()
                
                # Save TTF/OTF to temp file (PIL needs file path, not bytes)
                temp_font = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(item_name)[1])
                temp_font.write(font_data)
                temp_font.close()

                # Extract font family name from filename
                font_name = os.path.splitext(os.path.basename(item_name))[0]
                custom_fonts[font_name] = temp_font.name
            except Exception as e:
                print(f"Failed to extract font {item.get_name()}: {e}")

    return custom_fonts   

def get_images(book:epub.EpubBook) -> dict[str, Image.Image]:
    """Extract all images from EPUB and cache them (including SVG conversion)"""

    images:dict[str, Image.Image] = {}

    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        img_name = item.get_name()
        img_data = item.get_content()
        img = convert_images(img_name, img_data)

        if(img):
            images[img_name] = img
            
    return images

def parse_html(html: str) -> list[TextToken | ImageToken | TableToken]:
    token_list:list[TextToken | ImageToken | TableToken] = []

    # Remove metadata
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['head', 'script', 'style', 'title', 'meta']):
        tag.decompose()

    def process_node(node, current_style='normal', current_align='left'):
        if isinstance(node, NavigableString):
            text = str(node).replace('\n', ' ').strip()
            if not text: return

            words = re.split(r'(\s+)', str(node).replace('\n', ' '))
            for w in words:
                if w:
                    token_list.append(TextToken(w, current_style, False, current_align))
            return

    return token_list

def process_node(node, tokens:list[TextToken | ImageToken | TableToken], *,
                 text_width:int, text_height:int, current_style='normal', current_align='left'):
    if isinstance(node, NavigableString):
        text = str(node).replace('\n', ' ').strip()
        if not text: return

        words = re.split(r'(\s+)', str(node).replace('\n', ' '))
        for w in words:
            if w:
                tokens.append(TextToken(w, current_style, False, current_align))
        return

    if isinstance(node, Tag):
        # Handle table tags
        if node.name == 'table':
            rows = []
            for tr in node.find_all('tr'):
                cells = []
                for cell in tr.find_all(['td', 'th']):
                    # Extract text from cell, preserving basic formatting
                    cell_text = cell.get_text(separator=' ', strip=True)
                    cells.append(cell_text)
                if cells:
                    rows.append(cells)

            if rows:
                tokens.append(TableToken(rows, text_width))
            return  # Don't process children of table tag

        # Handle image tags
        if node.name == 'img':
            src = node.get('src', '')
            if src:
                # Normalize path (remove ../ and leading /)
                img_path = src.split('/')[-1]  # Get just the filename

                # Try to find image in cache
                img = None
                for key in self.images.keys():
                    if key.endswith(img_path) or img_path in key:
                        img = self.images[key]
                        break

                if img:
                    # Add image token with max dimensions
                    max_img_width = self.text_width
                    max_img_height = int(self.text_height * 0.6)  # Max 60% of page height
                    tokens.append(ImageToken(img, max_img_width, max_img_height))
                    self.logger.debug(f"Added image token: {img_path}")
                else:
                    self.logger.warning(f"Image not found in EPUB: {src}")
            return  # Don't process children of img tag

        style = current_style
        align = current_align
        is_block = node.name in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'br', 'li']

        # Check for CSS text-align in style attribute
        node_style = node.get('style', '')
        if 'text-align' in node_style:
            if 'center' in node_style:
                align = 'center'
            elif 'right' in node_style:
                align = 'right'
            elif 'left' in node_style:
                align = 'left'

        # Check for center tag
        if node.name == 'center':
            align = 'center'

        # Determine style
        if node.name in ['b', 'strong']:
            style = 'bold_italic' if 'italic' in style else 'bold'
        elif node.name in ['i', 'em']:
            style = 'bold_italic' if 'bold' in style else 'italic'
        elif node.name == 'h1':
            style = 'h1'
            align = 'center'  # Headers are typically centered
        elif node.name == 'h2':
            style = 'h2'
            align = 'center'  # Headers are typically centered
        elif node.name in ['h3', 'h4']:
            style = 'bold'

        if is_block and tokens and not tokens[-1].new_paragraph:
            # Mark last token to end paragraph
            if isinstance(tokens[-1], TextToken):
                tokens[-1] = tokens[-1]._replace(new_paragraph=True)

        for child in node.children:
            process_node(child, style, align)

        if is_block and tokens and not tokens[-1].new_paragraph:
            # Mark last token to end paragraph
            if isinstance(tokens[-1], TextToken):
                tokens[-1] = tokens[-1]._replace(new_paragraph=True)

def load_book(book:epub.EpubBook):
    all_tokens = []

    docs:list[epub.EpubItem] = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    total_docs = len(docs)

    for idx, item in enumerate(docs[:10]):        
        try:
            content = item.get_content()
            try:
                html = content.decode('utf-8')
            except UnicodeDecodeError:
                html = content.decode('latin-1', errors='ignore')

            tokens = parse_html(html)
            if tokens:
                all_tokens.extend(tokens)
                all_tokens.append(TextToken("", "normal", new_paragraph=True))
        except Exception as e:
            print(f"Chapter error: {e}")

    

if __name__ == "__main__":
    book = epub.read_epub(os.path.join(BOOK_PATH, BOOK_NAME))

    print(book.get_metadata('DC', 'title'))
    md = book.get_metadata('OPF', 'cover')
    oit:epub.Link = book.toc[0]
    # for it in book.toc:
    #     print(f"href: {it.href}, title:{it.title}")

    image_map = get_images(book)
    keys = list(image_map.keys())

    for k in keys[:5]:
        print(f"name: {k} : {image_map[k].size}")

    cover = get_cover(book)
    print(f"cover : {"no dice" if cover is None else cover.size}")

    print(f"fonts {get_embeded_fonts(book)}")
    load_book(book)


# ITEM_UNKNOWN
# ITEM_IMAGE
# ITEM_STYLE
# ITEM_SCRIPT
# ITEM_NAVIGATION
# ITEM_VECTOR
# ITEM_FONT
# ITEM_VIDEO
# ITEM_AUDIO
# ITEM_DOCUMENT
# ITEM_COVER
# ITEM_SMIL