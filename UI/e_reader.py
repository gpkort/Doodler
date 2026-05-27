from typing import Callable
from PIL import Image

from UI import AppController
from display.display_driver import DisplayDriver
from input.dispatcher import EventDispatcher
from data import Book, get_books
from UI import IconInfo, IconInputHandler

class EReaderController(AppController):
    def __init__(self, display: DisplayDriver, 
                 event_dispatcher: EventDispatcher, 
                 exit_callback: Callable[[], None],
                 home_screen_image: Image.Image):
        super().__init__(display, event_dispatcher, exit_callback, home_screen_image)

        self.books: list[Book] = get_books()
        book_info:list[list[IconInfo]] = []

        j:int = 0
        for i, book in enumerate(self.books):
            if i % 4 == 0:
                book_info.append([])
                j = 0
            
            book_info[-1].append(IconInfo(name=book.title, icon_path=book.thumbnail_path))
            j += 1

        
        self.icon_input_handler: IconInputHandler = IconInputHandler(self.display, 
                                                                     book_info, home_screen_image,
                                                                     icon_width=36, icon_height=72)

    @staticmethod
    def get_name() -> str:
        return "E-Reader"

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