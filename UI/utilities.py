from abc import ABC, abstractmethod
import logging
from tkinter import Event
from typing import Callable
from dataclasses import dataclass
import uuid

from PIL import Image

from display import DisplayDriver
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
                 show_on_start: bool = True,
                 top_x: int = 60,
                 data:dict | None = None):
        
        self.display: DisplayDriver = display
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.exit_callback: Callable[[], None] = exit_callback
        self.event_uuids: list[uuid.UUID] = []
        self.home_screen_image: Image.Image | None = home_screen_image
        self.top_x = top_x
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data: dict = data or {}
        
        if show_on_start and self.home_screen_image:
            self.draw(self.home_screen_image)
    
    
    def draw(self, image: Image.Image):
        self.display.draw_image(image)  # type: ignore
        
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
    
    
    



