from abc import ABC, abstractmethod
from PIL import Image

TOP_FOR_ICONS: int = 60
LEFT_MARGIN: int = 10
RIGHT_MARGIN: int = 470

ICON_WIDTH:int = 36
ICON_HEIGHT:int = 36
ICON_SPACE:int = 10

class DisplayDriver(ABC):
    """Abstract base class for display"""
    
    @abstractmethod
    def initialize(self)->None:
        pass
    
    @abstractmethod
    def clear(self)->None:
        pass
    
    @abstractmethod
    def display_image(self, image: Image.Image, use_partial: bool = True, skip_counter: bool = False)->None:
        pass
    
    @abstractmethod
    def sleep(self)->None:
        pass
    
    @abstractmethod
    def cleanup(self)->None:
        pass
    