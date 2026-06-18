from dataclasses import dataclass
from io import BytesIO
import re

import ebooklib
from ebooklib import epub
from PIL import Image, ImageDraw, ImageFont, ImageFile

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

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

# Define a table token for HTML tables
@dataclass
class TableToken:
    rows: list[list[str]]  # 2D array of cell contents
    max_width: int  # Maximum width for table
    new_paragraph: bool = True


FONT_CANIDATES: list[dict[str, str]] = [
        # DejaVu Serif (common on Raspberry Pi)
        {
            'normal': '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
            'bold': '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
            'italic': '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf',
            'bold_italic': '/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf',
        },
        # Liberation Serif
        {
            'normal': '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
            'bold': '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
            'italic': '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf',
            'bold_italic': '/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf',
        },
        # Windows fonts
        {
            'normal': 'C:/Windows/Fonts/times.ttf',
            'bold': 'C:/Windows/Fonts/timesbd.ttf',
            'italic': 'C:/Windows/Fonts/timesi.ttf',
            'bold_italic': 'C:/Windows/Fonts/timesbi.ttf',
        },
    ]

def load_fonts(candidates: list[dict[str, str]], *, base_size = 18, header_size:int = 24, zoom:float=1.0) -> dict[str, ImageFont.ImageFont | ImageFont.FreeTypeFont]:
    """Load specific TrueType fonts for styles"""

    base_font_size = int(base_size * zoom)
    header_font_size = int(header_size * zoom)
    fonts : dict[str, ImageFont.ImageFont | ImageFont.FreeTypeFont] = {}
    # Find first available font family
    font_paths : dict[str, str] | None = None

    for candidate in candidates:
        if os.path.exists(candidate['normal']):
            font_paths = candidate
            print(f"Using font: {candidate['normal']}")
            break

    if not font_paths:
        print("No TrueType fonts found, using default bitmap font")
        default = ImageFont.load_default()
        fonts = {k: default for k in ['normal', 'bold', 'italic', 'bold_italic', 'h1', 'h2']}
        return fonts

    # Load fonts with fallback to normal if variants don't exist
    def load_font(style, size):
        path = font_paths.get(style, font_paths['normal'])
        if not os.path.exists(path):
            path = font_paths['normal']  # Fallback to normal
        try:
            return ImageFont.truetype(path, size)
        except Exception as e:
            print(f"Failed to load {path}: {e}")
            return ImageFont.load_default()

    fonts['normal'] = load_font('normal', base_font_size)
    fonts['bold'] = load_font('bold', base_font_size)
    fonts['italic'] = load_font('italic', base_font_size)
    fonts['bold_italic'] = load_font('bold_italic', base_font_size)
    fonts['h1'] = load_font('bold', header_font_size)
    fonts['h2'] = load_font('bold', int(header_font_size * 0.9))

    return fonts

def get_images(book:epub.EpubBook) -> dict[str, Image.Image | ImageFile.ImageFile]:

    images : dict[str, Image.Image | ImageFile.ImageFile] = {}
    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        try:
            img_name = item.get_name()
            img_data = item.get_content()

            # Check if this is an SVG file
            if img_name.lower().endswith('.svg'):
                if SVG_SUPPORT:
                    try:
                        # Convert SVG to PNG using cairosvg
                        png_data = cairosvg.svg2png(bytestring=img_data, output_width=800) #type: ignore
                        img = Image.open(BytesIO(png_data))   #type: ignore                         
                    except Exception as e:
                        print(f"Failed to convert SVG {img_name}: {e}")
                        continue
                else:
                    print(f"SVG support not available (install cairosvg): {img_name}")
                    continue
            else:
                # Regular raster image (PNG, JPG, GIF, etc.)
                img = Image.open(BytesIO(img_data))

            # Convert to appropriate mode for e-ink
            if img.mode == 'RGBA':
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                img = background
            elif img.mode not in ['RGB', 'L', '1']:
                img = img.convert('RGB')

            # Store with filename as key
            images[img_name] = img                
        except Exception as e:
            print(f"Failed to extract image {item.get_name()}: {e}")

    return images

def extract_fonts(book: epub.EpubBook) -> dict[str, str]:
    """Extract embedded fonts from EPUB"""
    import tempfile

    custom_fonts: dict[str, str] = {}

    for item in book.get_items():
        # Check if this is a font file (TTF, OTF, WOFF, etc.)
        item_name = item.get_name().lower()
        if any(item_name.endswith(ext) for ext in ['.ttf', '.otf', '.woff', '.woff2']):
            try:
                font_data = item.get_content()

                # WOFF/WOFF2 fonts need conversion (skip for now - complex)
                if item_name.endswith(('.woff', '.woff2')):
                    print(f"Skipping WOFF font (conversion not supported): {item.get_name()}")
                    continue

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

def load_custom_fonts(custom_fonts: dict[str, str], 
                      fonts:dict[str, ImageFont.ImageFont | ImageFont.FreeTypeFont], 
                      *, base_size = 18, header_size:int = 24, zoom:float=1.0):
        """Try to load custom EPUB fonts for rendering"""

        base_font_size = int(base_size * zoom)
        header_font_size = int(header_size * zoom)

        # Look for fonts that might replace our default fonts
        for font_name, font_path in custom_fonts.items():
            font_name_lower = font_name.lower()

            # Try to match to our font styles
            try:
                if 'bolditalic' in font_name_lower or 'bold-italic' in font_name_lower:
                    fonts['bold_italic'] = ImageFont.truetype(font_path, base_font_size)
                elif 'bold' in font_name_lower:
                    fonts['bold'] = ImageFont.truetype(font_path, base_font_size)
                    fonts['h1'] = ImageFont.truetype(font_path, header_font_size)
                    fonts['h2'] = ImageFont.truetype(font_path, int(header_font_size * 0.9))
                elif 'italic' in font_name_lower:
                    fonts['italic'] = ImageFont.truetype(font_path, base_font_size)
                elif 'regular' in font_name_lower or 'normal' in font_name_lower or len(custom_fonts) == 1:
                    # Use as default font if it's marked as regular/normal or it's the only font
                    fonts['normal'] = ImageFont.truetype(font_path, base_font_size)
            except Exception as e:
                print(f"Failed to load custom font {font_name}: {e}")

def parse_html(self, html: str) -> list[TextToken | ImageToken | TableToken]:
        """Parse HTML into flat list of tokens with styles"""
        soup = BeautifulSoup(html, 'html.parser')
        tokens: list[TextToken | ImageToken | TableToken] = []

        # Remove metadata
        for tag in soup(['head', 'script', 'style', 'title', 'meta']):
            tag.decompose()

        def process_node(node, current_style='normal', current_align='left'):
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
                        tokens.append(TableToken(rows, self.text_width))
                        self.logger.debug(f"Added table token: {len(rows)} rows")
                    return  # Don't process children of table tag

                # Handle image tags
                if node.name == 'img':
                    src = node.get('src', '')
                    if src is not None:
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

        process_node(soup.body if soup.body else soup)
        return tokens

if __name__ == "__main__":
    book = epub.read_epub(os.path.join(BOOK_PATH, BOOK_NAME))
    images_dict = get_images(book)
    custom_font_dict = extract_fonts(book)
    fonts = load_fonts(FONT_CANIDATES)
    print(len(book.pages))
    print(len(images_dict))
    print(len(custom_font_dict))
    print(fonts.keys())
    x = 0