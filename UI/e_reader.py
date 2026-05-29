from typing import Callable
from PIL import Image, ImageDraw, ImageFont

from UI import AppController
from display import DisplayDriver, fontmanager, SCREEN_HEIGHT, SCREEN_WIDTH, LEFT_MARGIN
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
        self.create_book_buttons()
        
    @staticmethod
    def get_name() -> str:
        return "E-Reader"
    
    def create_book_buttons(self) -> list[list[IconInfo]]:
        self.books = get_books()
        icons: list[list[IconInfo]] = []
        current_y: int = 60  # Starting y position for the first book

        for book in self.books:
            if current_y == 60:
                icons.append([])
            font = fontmanager.medium_font
            left, top, right, bottom = font.getbbox(book.title)
            height = bottom - top
            text_x = (SCREEN_WIDTH - (right - left)) / 2
            list_image: Image.Image = Image.new("1", (SCREEN_WIDTH, int(height + 10)), color="white")
            draw = ImageDraw.Draw(list_image)
            draw.text((text_x, 5), book.title, font=font, fill=0)
            current_y += int(height + 10)

            icons[0].append(IconInfo(book.title, list_image))

            if current_y + int(height + 10) > SCREEN_HEIGHT - 20:
                current_y = 60


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