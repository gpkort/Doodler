from collections.abc import Callable
from enum import Enum
from dataclasses import dataclass
from typing import Any
import uuid

class Event(Enum):
    FORWARD = 1
    BACKWARD = 2
    UP = 3
    DOWN = 4    
    ENTER = 5
    QUIT = 6
    APP_BACK = 7
    UNKNOWN = 99

@dataclass
class EventHandler:
    event_type: Event
    handler: Callable[[dict[str, Any]], None]

class EventDispatcher:
    def __init__(self):
        self.handlers: dict[uuid.UUID, EventHandler] = {}
    
    def register_handler(self, event_handler: EventHandler) -> uuid.UUID:
        handler_id = uuid.uuid4()
        self.handlers[handler_id] = event_handler
        return handler_id
    
    def unregister_handler(self, handler_id: uuid.UUID):
        if handler_id in self.handlers:
            del self.handlers[handler_id]
    
    def _dispatch(self, event:Event, data: dict[str, Any] = {}): #ignore 
        if data is None:
            data = {}
        for handler in self.handlers.values():
            if handler.event_type == event:
                handler.handler(data)