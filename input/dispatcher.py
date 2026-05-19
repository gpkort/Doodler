from collections.abc import Callable
from enum import Enum
from dataclasses import dataclass
from typing import Any

class Event(Enum):
    FORWARD = 1
    BACKWARD = 2
    UP = 3
    DOWN = 4    
    ENTER = 5
    QUIT = 6
    UNKNOWN = 99

@dataclass
class EventHandler:
    event_type: Event
    handler: Callable[[dict[str, Any]], None]

class EventDispatcher:
    def __init__(self):
        self.handlers: list[EventHandler] = []
    
    def register_handler(self, event_handler: EventHandler):
        self.handlers.append(event_handler)
    
    def _dispatch(self, event:Event, data: dict[str, Any] = {}): #ignore 
        if data is None:
            data = {}
        for handler in self.handlers:
            if handler.event_type == event:
                handler.handler(data)