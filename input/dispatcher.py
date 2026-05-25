from collections.abc import Callable
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Any
import uuid

class Event(Enum):
    FORWARD = 1
    BACKWARD = 2
    UP = 3
    DOWN = 4
    RIGHT = 5
    LEFT = 6
    ENTER = 7
    QUIT = 8
    APP_BACK = 9
    UNKNOWN = 99

@dataclass
class EventHandler:
    event_type: Event
    handler: Callable[[dict[str, Any]], None]

class EventDispatcher(ABC):
    def __init__(self):
        self.event_handlers: dict[uuid.UUID, EventHandler] = {}
        
    @abstractmethod
    def create_buttons(self):
        pass
    
    def register_handler(self, event_handler: EventHandler) -> uuid.UUID:
        handler_id = uuid.uuid4()
        self.event_handlers[handler_id] = event_handler
        return handler_id
    
    def register_handlers(self, event_handlers: list[EventHandler]) -> list[uuid.UUID]:
        handler_ids = []
        for event_handler in event_handlers:
            handler_id = self.register_handler(event_handler)
            handler_ids.append(handler_id)
        return handler_ids
    
    def unregister_handler(self, handler_id: uuid.UUID) -> list[uuid.UUID]:
        if handler_id in self.event_handlers:
            del self.event_handlers[handler_id]
        return list(self.event_handlers.keys())
            
    def unregister_handlers(self, handler_ids: list[uuid.UUID]) -> list[uuid.UUID]:
        for handler_id in handler_ids:
            self.unregister_handler(handler_id)
        return list(self.event_handlers.keys())
    
    def unregister_all_handlers(self) -> None:
        self.event_handlers.clear()
    
    def _dispatch(self, event:Event, data: dict[str, Any] | None = None): #ignore 
        if data is None:
            data = {}
            
        for handler in self.event_handlers.values():
            if handler.event_type == event:
                handler.handler(data)
    
    
                
    