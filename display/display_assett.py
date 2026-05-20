from logging import config

from PIL import ImageFont, Image
from dataclasses import dataclass
from enum import Enum
from os import path



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
    def small_font(self) -> ImageFont.FreeTypeFont | None:
        return self.fonts.get(FontSize.SMALL)
    @property
    def medium_font(self) -> ImageFont.FreeTypeFont | None:
        return self.fonts.get(FontSize.MEDIUM) 
    @property
    def large_font(self) -> ImageFont.FreeTypeFont | None:
        return self.fonts.get(FontSize.LARGE)

    def get_font(self, size: FontSize) -> ImageFont.FreeTypeFont | None:
        return self.fonts.get(size)
    
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
#  icons: list[str] = ["home.png", "audio.png", "mp3.png", "settings.png", "ereader.png"]
#     size = 128, 128

#     for icon in icons:
#         file = path.join("assets", "icons", icon)
#         save_file = path.join("assets", "thumbnails", icon[:-4] + "_tn.png")
#         with Image.open(file) as im:
#             im.thumbnail(size)
#             im.save(save_file, "PNG")
       