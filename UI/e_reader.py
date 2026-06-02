from typing import Callable
from PIL import Image, ImageDraw, ImageFont

from UI import AppController
from display import DisplayDriver, fontmanager, SCREEN_HEIGHT, SCREEN_WIDTH
from input import EventDispatcher, EventHandler, Event
from data import Book, get_books
from UI import IconInfo, IconInputHandler, IconLayout

class EReaderController(AppController):
    def __init__(self, display: DisplayDriver, 
                 event_dispatcher: EventDispatcher, 
                 exit_callback: Callable[[], None],
                 home_screen_image: Image.Image):
        super().__init__(display, event_dispatcher, exit_callback, home_screen_image)

        self.register_app_controller()

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
            list_image: Image.Image = Image.new("1", (SCREEN_WIDTH - 30, int(height + 10)), color="white")
            draw = ImageDraw.Draw(list_image)
            draw.text((text_x, 5), book.title, font=font, fill=0)
            
            icons.append(IconInfo(name=book.title, 
                                   icon=list_image))
            
        return icons
    
    def register_app_controller(self) :
        self.event_ids.clear()
        print(f"Listeners before count: {len(self.event_dispatcher.event_handlers)}")
        
        self.event_ids.append(self.event_dispatcher.register_handler(EventHandler(Event.FORWARD, self.forward)))
        self.event_ids.append(self.event_dispatcher.register_handler(EventHandler(Event.BACKWARD, self.backward)))
        self.event_ids.append(self.event_dispatcher.register_handler(EventHandler(Event.UP, self.up, blocking=True)))
        self.event_ids.append(self.event_dispatcher.register_handler(EventHandler(Event.DOWN, self.down, blocking=True)))
        self.event_ids.append(self.event_dispatcher.register_handler(EventHandler(Event.LEFT, self.left, blocking=True)))
        self.event_ids.append(self.event_dispatcher.register_handler(EventHandler(Event.RIGHT, self.right, blocking=True)))
        self.event_ids.append(self.event_dispatcher.register_handler(EventHandler(Event.ENTER, self.enter, blocking=True)))
        
        print(f"Listeners after count: {len(self.event_dispatcher.event_handlers)}")
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