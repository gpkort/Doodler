from abc import ABC, abstractmethod
from PIL import Image

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
    
class IconDisplayManager:
    def __init__(self, display: DisplayDriver):
        self.display = display
