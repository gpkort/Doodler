from typing import Callable
from PIL import Image, ImageDraw, ImageFont

from UI import AppController
from display import DisplayDriver, fontmanager, SCREEN_HEIGHT, SCREEN_WIDTH
from input.dispatcher import EventDispatcher
from data import Book, get_books
from UI import IconInfo, IconInputHandler, IconLayout

class EReaderController(AppController):
    def __init__(self, display: DisplayDriver, 
                 event_dispatcher: EventDispatcher, 
                 exit_callback: Callable[[], None],
                 home_screen_image: Image.Image):
        super().__init__(display, event_dispatcher, exit_callback, home_screen_image)

        self.books: list[Book] = []
        self.icon_input_handler: IconInputHandler = IconInputHandler(self.create_book_buttons(),
                                                                     self.home_screen_image,
                                                                     icon_layout=IconLayout.VERTICAL_LIST)
        
        img: Image.Image | None = self.icon_input_handler.draw_current_selection()
        if img:
            self.display.display_image(img)
        
    @staticmethod
    def get_name() -> str:
        return "E-Reader"
    
    def create_book_buttons(self) -> list[IconInfo]:
        self.books = get_books()
        icons: list[IconInfo] = []
        
        for book in self.books:
            font = fontmanager.medium_font
            left, top, right, bottom = font.getbbox(book.title)
            height = bottom - top
            text_x = (SCREEN_WIDTH - (right - left)) / 2
            list_image: Image.Image = Image.new("1", (SCREEN_WIDTH -10, int(height + 10)), color="white")
            draw = ImageDraw.Draw(list_image)
            draw.text((text_x, 5), book.title, font=font, fill=0)
            
            icons.append(IconInfo(name=book.title, 
                                   icon=list_image))
            
        return icons
        

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