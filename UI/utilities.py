from abc import ABC, abstractmethod
from typing import Callable

from display import DisplayDriver
from input import EventDispatcher

class AppController(ABC):
    @staticmethod
    def get_name() -> str:
        return "BaseApp"
    def __init__(self, display: DisplayDriver, event_dispatcher: EventDispatcher, exit_callback: Callable[[], None]):
        self.display: DisplayDriver = display
        self.event_dispatcher = event_dispatcher
        self.exit_callback = exit_callback
        
    @abstractmethod
    def handle_event(self, event: dict):
        pass



