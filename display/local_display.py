from display.display import Display
from PIL import Image


class LocalDisplay(Display):
    def __init__(self, display_width: int, display_height: int):
        super().__init__(display_width, display_height)
        self.display_image: Image.Image = Image.new('RGB', (self.display_width, self.display_height))

    def init(self):
        pass

    def display(self, image:bytes):
        self.display_image = Image.frombytes('RGB',
                                             (self.display_width, self.display_height), 
                                             image)
        self.display_image.show()