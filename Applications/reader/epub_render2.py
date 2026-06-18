import io
# from pathlib import Path
import os
import ebooklib
from ebooklib import epub
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFile

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