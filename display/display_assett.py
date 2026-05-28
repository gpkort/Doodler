from logging import config
import os

from PIL import ImageFont, Image, ImageDraw
from dataclasses import dataclass
from enum import Enum
from os import path, remove



class FontSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

@dataclass
class FontConfig:
    path: str
    name: str
    font_size: FontSize
    actual_size: int

class _FontManager:
    _isInit: bool

    def __init__(self):
        self.fonts: dict[FontSize, ImageFont.FreeTypeFont] = {}

    def initialize(self, config: list[FontConfig]) -> None:
        for fc in config:
            self.fonts[fc.font_size] = ImageFont.truetype(path.join(fc.path, fc.name), fc.actual_size)

        _FontManager._isInit = True

    @staticmethod
    def isInitialized() -> bool:
        return _FontManager._isInit

    @property
    def small_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        return self.fonts.get(FontSize.SMALL, ImageFont.load_default_imagefont())
    @property
    def medium_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        return self.fonts.get(FontSize.MEDIUM, ImageFont.load_default_imagefont())
    @property
    def large_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        return self.fonts.get(FontSize.LARGE, ImageFont.load_default_imagefont())

    def get_font(self, size: FontSize) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        return self.fonts.get(size, ImageFont.load_default_imagefont())
    
class _IconManager:
    _isInit: bool

    def __init__(self,):        
        self.icons: dict[str, Image.Image] = {}

    @staticmethod
    def isInitialized() -> bool:
        return _IconManager._isInit
    
    def initialize(self, config:dict[str, str]) -> None:
        self.icons.clear()
        for name, path in config.items():
            self.icons[name] = Image.open(path)
        _IconManager._isInit = True

    def get_icon(self, name: str) -> Image.Image | None:
        return self.icons.get(name)
    
    def get_icon_names(self) -> list[str]:
        return list(self.icons.keys())

  
iconmanager = _IconManager()
fontmanager = _FontManager()

def make_icons():
    icons: list[str] = ["home.png", "audio.png", "mp3.png", "settings.png", "ereader.png"]
    size = 64, 64

    for icon in icons:
        file = path.join("assets", "icons", icon)
        save_file = path.join("assets", "thumbnails","normal", icon[:-4] + "_n.png")
        if(os.path.exists(save_file)):
                os.remove(save_file)
        with Image.open(file) as im:            
            im.thumbnail(size)
            im.save(save_file, "PNG")
    for icon in icons:
        file = path.join("assets", "thumbnails", "normal", icon[:-4] + "_n.png")
        save_file = path.join("assets", "thumbnails", "chosen", icon[:-4] + "_c.png")
        newicon = Image.new('1', (74, 74), 255)
        im = Image.open(file)
        draw = ImageDraw.Draw(newicon)
        draw.rectangle((2, 2, 72, 72), outline="black", width=2, fill=None)
        newicon.paste(im, (4, 4))
        if(os.path.exists(save_file)):
                os.remove(save_file)
        
        newicon.save(save_file, "PNG")
    
    # def getHomeImage(self) -> Image.Image:
    #     Himage = Image.new('1', (480, 740), 255)
    #     for row in HOME_SCREEN_ICONS:
    #         for button in row:
    #             icon = Image.open(button.unselected_file_path)
    #             Himage.paste(icon, (button.x, button.y))

    #     Himage.save(os.path.join("assets", "screens", "home_screen.png"), "PNG")
    #     return Himage    
        
    def make_base_image(self, width:int = 480, height:int = 800) -> None:
        # Create and return the image to be displayed on the home screen
        top:int = 5
        r_margin:int = 470
        l_margin:int = 10
        space:int = 30
        font = self.font_manager.get_font(FontSize.LARGE) or ImageFont.load_default()

        names:dict[str, str] = {"E-Reader": "assets/icons/book.png",
                                "Audio Books": "assets/thumbnails/normal/audio_n.png", 
                                "MP3": "assets/thumbnails/normal/mp3_n.png", 
                                "Settings": "assets/thumbnails/normal/settings_n.png"}
        
        for name, path in names.items():
            icon:Image.Image = Image.open(path)
            arrow:Image.Image = Image.open("assets/icons/back.png")
            icon = icon.resize((36, 36))
            arrow = arrow.resize((36, 36))
            icon_width, icon_height = icon.size
            arrow_width, arrow_height = arrow.size
            print(f"Icon size: {icon_width}x{icon_height}")
            print(f"arrow size: {arrow_width}x{arrow_height}")          
            Himage = Image.new('1', (width, height), 255)
            draw = ImageDraw.Draw(Himage)
        
            #Header
            title:str = name
            _, ttop, _, tbottom = font.getbbox(title)
            
            ty:int = (int)(top + (icon_height - (tbottom - ttop)) // 2)
            line_y:int = (int)(max(icon_height, ttop - top)) + 15
            Himage.paste(arrow, (l_margin, top))
            current_x = l_margin + arrow_width + 10
            draw.line((current_x + 10, top, current_x + 10, line_y), fill=0, width=2)
            current_x += 10 
            Himage.paste(icon, (current_x + 10, top))
            current_x += icon_width + space
            draw.text((current_x, ty), f"{title}", font = font, fill = "black", width=2  ) #120
            draw.line((l_margin, line_y, r_margin, line_y), fill = 0) # y=45

            print(f"Header text position: ({current_x}, {ty}), line_y: {line_y}")

            save_path = os.path.join("assets", "screens", "base",f"{name.lower()}_basescreen.png")
            Himage.save(save_path, "PNG")
       