from display.display import Display
from lib.epd7in5_V2 import EPD


class EpaperDisplay(Display):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.epd = EPD()

    def reset (self):
        self.epd.reset()
    def init (self):
        self.epd.init()
    def init_fast (self):
        self.epd.init_fast()
    def display (self, image:bytes):
        self.epd.display(image)
    def init_4Gray (self):
        self.epd.init_4Gray()
    def display_Partial(self, image):
        self.epd.display_Partial(image)
    def display_4Gray(self, image):
        self.epd.display_4Gray(image)
    def Clear(self):
        self.epd.Clear()
    def sleep(self):
        self.epd.sleep()