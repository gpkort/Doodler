from abc import ABC, abstractmethod
import logging
from tkinter import Event
from typing import Callable
from dataclasses import dataclass
import uuid
from enum import Enum

from PIL import Image, ImageDraw

from display import DisplayDriver, TOP_FOR_ICONS, LEFT_MARGIN, RIGHT_MARGIN
from display.utilities import ICON_HEIGHT, ICON_SPACE, ICON_WIDTH
from input import EventDispatcher, EventHandler, Event
from input.dispatcher import EventHandler

@dataclass
class AppInfo:
    app_class: type["AppController"]
    base_image_path: str

class AppController(ABC):
    def __init__(self, display: DisplayDriver,
                 event_dispatcher: EventDispatcher,
                 exit_callback: Callable[[], None],   
                 home_screen_image: Image.Image | None = None,
                 data:dict | None = None):
        
        self.display: DisplayDriver = display
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.exit_callback: Callable[[], None] = exit_callback
        self.event_uuids: list[uuid.UUID] = []
        self.home_screen_image: Image.Image | None = home_screen_image
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data: dict = data or {}
        
        
    
    
    def draw(self, image: Image.Image):
        self.display.display_image(image)  # type: ignore
        
    def register_app_controller(self) :
        self.event_uuids.clear()
        
        self.event_dispatcher.register_handler(EventHandler(Event.FORWARD, self.forward))
        self.event_dispatcher.register_handler(EventHandler(Event.BACKWARD, self.backward))
        self.event_dispatcher.register_handler(EventHandler(Event.UP, self.up))
        self.event_dispatcher.register_handler(EventHandler(Event.DOWN, self.down))
        self.event_dispatcher.register_handler(EventHandler(Event.LEFT, self.left))
        self.event_dispatcher.register_handler(EventHandler(Event.RIGHT, self.right))
        self.event_dispatcher.register_handler(EventHandler(Event.ENTER, self.enter))
        self.event_dispatcher.register_handler(EventHandler(Event.QUIT, self.quit))
    
    def unregister_app_controller(self):
        self.event_dispatcher.unregister_all_handlers()
        self.event_uuids.clear()
       
    @abstractmethod
    def handle_event(self, event: dict):
        pass
    
    @abstractmethod
    def forward(self, data: dict):
        pass
    
    @abstractmethod
    def backward(self, data: dict):
        pass
    
    @abstractmethod    
    def up(self, data: dict):
        pass    
    
    @abstractmethod
    def down(self, data: dict):
        pass
    
    @abstractmethod
    def right(self, data: dict):
        pass
    
    @abstractmethod
    def left(self, data: dict):
        pass
    
    @abstractmethod
    def enter(self, data: dict):
        pass
    
    @abstractmethod
    def quit(self, data: dict):
        pass
    

@dataclass
class IconInfo:
    name: str
    icon_path: str

class IconInputHandler:
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4
        
    def __init__(self, display: DisplayDriver, 
                 buttons: list[list[IconInfo]],
                 base_image: Image.Image, 
                 row_index: int = -1, 
                 column_index: int = -1,
                 top: int = TOP_FOR_ICONS,
                 left: int = LEFT_MARGIN,
                 right: int = RIGHT_MARGIN,
                 icon_width: int = ICON_WIDTH,
                 icon_height: int = ICON_HEIGHT,
                 icon_space: int = ICON_SPACE):
        
        self.display = display
        self.buttons = buttons
        self.row_index = row_index
        self.column_index = column_index
        self.top = top
        self.left = left
        self.right = right
        self.base_image = base_image
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.icon_space = icon_space

        self.draw_current_selection()

    @property
    def current_button(self) -> IconInfo | None:
        if self.row_index == -1 or self.column_index == -1:
            return None
        return self.buttons[self.row_index][self.column_index]
    
    @property
    def current_row_index(self) -> int:
        return self.row_index
    @property
    def current_column_index(self) -> int:
        return self.column_index

    def direction_change(self, direction: Direction) -> IconInfo :
        if self.row_index == -1 or self.column_index == -1:
            self.row_index = 0
            self.column_index = 0
            return self.buttons[self.row_index][self.column_index]
    
        if direction == IconInputHandler.Direction.UP:
            self.row_index = self.row_index - 1 if self.row_index > 0 else len(self.buttons) - 1
            self.draw_current_selection()
        elif direction == IconInputHandler.Direction.DOWN:
            self.row_index = self.row_index + 1 if self.row_index < len(self.buttons) - 1 else 0
            self.draw_current_selection()
        elif direction == IconInputHandler.Direction.LEFT:
            self.column_index = self.column_index - 1 if self.column_index > 0 else len(self.buttons[self.row_index]) - 1
            self.draw_current_selection()   
        elif direction == IconInputHandler.Direction.RIGHT:
            self.column_index = self.column_index + 1 if self.column_index < len(self.buttons[self.row_index]) - 1 else 0
            self.draw_current_selection()

        return self.buttons[self.row_index][self.column_index]
    
    def draw_current_selection(self):
        current_x: int = self.left
        current_y: int = self.top
        new_image = self.base_image.copy()

        for i, row in enumerate(self.buttons):
            for j, button in enumerate(row):
                icon: Image.Image = Image.open(button.icon_path)
                icon = icon.resize((self.icon_width, self.icon_height))
                new_image.paste(icon, (current_x, current_y))                

                if i == self.row_index and j == self.column_index:
                    # Draw a border around the selected icon
                    draw = ImageDraw.Draw(new_image)
                    draw.rectangle(
                        [current_x - 3, current_y - 3, 
                         current_x + self.icon_width + 3, current_y + self.icon_height + 3],
                        outline="black",
                        width=2
                    )
                
                current_x += self.icon_width + self.icon_space

            current_x = self.left
            current_y += self.icon_height + self.icon_space
        self.display.display_image(new_image)
        
                  
    



