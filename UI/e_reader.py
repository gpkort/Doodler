from typing import Callable
from PIL import Image, ImageDraw, ImageFont

from UI import AppController
from display import DisplayDriver, fontmanager
from input.dispatcher import EventDispatcher
from data import Book, get_books
from UI import IconInfo, IconInputHandler

class EReaderController(AppController):
    def __init__(self, display: DisplayDriver, 
                 event_dispatcher: EventDispatcher, 
                 exit_callback: Callable[[], None],
                 home_screen_image: Image.Image):
        super().__init__(display, event_dispatcher, exit_callback, home_screen_image)

        self.books: list[Book] = []
        
    @staticmethod
    def get_name() -> str:
        return "E-Reader"
    
    def create_book_list(self) -> None:
        self.books = get_books()
        
        if self.home_screen_image is not None:
            draw = ImageDraw.Draw(self.home_screen_image)
            font = fontmanager.large_font 
            
            
            for idx, book in enumerate(self.books):
                len = font.getlength(book.title)
                x_position = 10 + len / 2
                draw.text((20, y_position), book.title, font=font, fill=0)
        

    def handle_event(self, event: dict):
        pass
    
    def forward(self, data: dict):
        pass
    
    def backward(self, data: dict):
        pass
    
    def up(self, data: dict):
        pass    
    
    def down(self, data: dict):
        pass
    
    def right(self, data: dict):
        pass
    
    def left(self, data: dict):
        pass
    
    def enter(self, data: dict):
        pass
    
    def quit(self, data: dict):
        pass