from abc import ABC, abstractmethod
import logging
from tkinter import Event
from typing import Callable
from dataclasses import dataclass
import uuid
from enum import Enum

from PIL import Image, ImageDraw

from display import (DisplayDriver, 
                     TOP_FOR_ICONS, 
                     LEFT_MARGIN, 
                     RIGHT_MARGIN,
                     SCREEN_WIDTH,
                     SCREEN_HEIGHT)
from input import EventDispatcher, EventHandler, Event
from input.dispatcher import EventHandler

ICON_SIDE = 36
ICON_SPACE = 15

COLUMN_COUNT = 5

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
        self.home_screen_image: Image.Image = home_screen_image or Image.new("1", 
                                                                             (SCREEN_WIDTH, SCREEN_HEIGHT), 
                                                                             color=1)  # Default to white background
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

class IconLayout(Enum):
    SIDE_BY_SIDE = 1
    VERTICAL_LIST = 2

class IconInfo():
    def __init__(self, name: str,
                 icon: str | Image.Image,
                 row: int = 0,
                 column: int = 0,
                 top: int=0, 
                 bottom: int=0,
                 right: int=0,
                 left: int=0):
        
        self._top = top
        self._bottom = bottom
        self._right = right
        self._left = left
        self.name = name
        self.row = row
        self.column = column
        self.page = -1
        
        if isinstance(icon, str):
            self.icon_path = icon
            self.img = Image.open(icon)
            
        else:
            self.img = icon

    @property
    def image(self) -> Image.Image:
        return self.img
    
    @property
    def top(self) -> int:
        return self._top
    
    @top.setter
    def top(self, value: int):
        self._top = value

    @property
    def bottom(self) -> int:
        return self._bottom
    
    @bottom.setter
    def bottom(self, value: int):
        self._bottom = value

    @property
    def right(self) -> int:
        return self._right

    @right.setter
    def right(self, value: int):
        self._right = value

    @property
    def left(self) -> int:
        return self._left

    @left.setter
    def left(self, value: int):
        self._left = value
        
    @property
    def cooridinate(self) -> tuple[int, int]:
        return (self.left, self.top)
    
    def set_coordinate(self, left: int, top: int):
        self.left = left
        self.top = top
        
    def set_row(self, row: int):
        self.row = row
        
    def set_column(self, column: int):
        self.column = column

class IconInputHandler:
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4
        
    def __init__(self,
                 buttons: list[IconInfo],
                 base_image: Image.Image,
                 *,
                 icon_layout: IconLayout = IconLayout.SIDE_BY_SIDE,
                 row_index: int = 0, 
                 column_index: int = 0,
                 top: int = TOP_FOR_ICONS,
                 left: int = LEFT_MARGIN,
                 right: int = RIGHT_MARGIN,
                 icon_side: int = ICON_SIDE,
                 icon_space: int = ICON_SPACE,
                 row_length: int = 0):
        
        self.buttons = buttons
        self.row_index = row_index
        self.column_index = column_index
        self.top = top
        self.left = left
        self.right = right
        self.base_image = base_image
        self.icon_side = icon_side
        self.icon_space = icon_space
        self.row_length = row_length
        self.column_length = COLUMN_COUNT
        
        self.icon_layout = icon_layout
        
        self.icon_pages: list[Image.Image] = self.draw_pages()

    @property
    def current_button(self) -> IconInfo | None:
        if self.row_index == -1 or self.column_index == -1:
            return None
        
        for button in self.buttons:
            if button.row == self.row_index and button.column == self.column_index:
                return button
        return None
    
    @property
    def current_row_index(self) -> int:
        return self.row_index
    @property
    def current_column_index(self) -> int:
        return self.column_index

    # TODO: bug when icon is last
    def direction_change(self, direction) -> None:
        if direction == IconInputHandler.Direction.UP:
            self.row_index = self.row_index - 1 if self.row_index > 0 else self.row_length - 1
        elif direction == IconInputHandler.Direction.DOWN:
            self.row_index = self.row_index + 1 if self.row_index < self.row_length - 1 else 0           
        elif direction == IconInputHandler.Direction.LEFT:
            self.column_index = self.column_index - 1 if self.column_index > 0 else self.column_length - 1           
        elif direction == IconInputHandler.Direction.RIGHT:
            self.column_index = self.column_index + 1 if self.column_index < self.column_length - 1 else 0
    
    def get_current_selection(self) -> IconInfo | None:
        for button in self.buttons:
            if button.row == self.row_index and button.column == self.column_index:
                return button
        return None
    
    def draw_current_selection(self) -> Image.Image | None:
        button = self.get_current_selection()
        
        if button is not None:
            page_image: Image.Image = self.icon_pages[button.page].copy()
            draw = ImageDraw.Draw(page_image)
            draw.rectangle(
                [button.left - 3, button.top - 3, 
                 button.left + self.icon_side + 3, button.top + self.icon_side + 3],
                outline="black",
                width=2
            )
            return page_image
        
        return None
    
    def draw_pages(self) -> list[Image.Image]:
        images: list[Image.Image] = []
        current_x: int = self.left
        current_y: int = self.top
        new_image = self.base_image.copy()
        row_count = 0 
        column_count = 0
        page: int = 0
        
        for button in self.buttons:
            icon = button.image
            
            if self.icon_layout == IconLayout.SIDE_BY_SIDE:
                icon = button.image.resize((self.icon_side, self.icon_side))       
                            
            new_image.paste(icon, (current_x, current_y))
            button.set_coordinate(current_x, current_y)
            button.set_row(row_count)
            button.set_column(column_count)
            button.page = page
            column_count += 1            
            
            if current_y + icon.height > SCREEN_HEIGHT - 10:
                images.append(new_image.copy())
                new_image = self.base_image.copy()
                current_x: int = self.left
                current_y: int = self.top
                self.row_length = row_count + 1
                column_count = 0
                row_count = 0
                page += 1
                continue
            
            if self.icon_layout == IconLayout.SIDE_BY_SIDE:
                current_x += self.icon_space + icon.width
                if column_count > self.column_length - 1:      # current_x > self.right:
                    column_count = 0
                    row_count += 1
                    current_x = self.left
                    current_y += self.icon_space + icon.height
            else:
                current_y += self.icon_space + icon.height
                current_x: int = self.left
                row_count += 1
                column_count = 1

        if new_image not in images:
            images.append(new_image.copy())
        return images
      
    



