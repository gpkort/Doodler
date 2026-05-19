from multiprocessing import Event
from collections.abc import Callable
import uuid
import logging

from input import EventDispatcher, Event, EventHandler
from UI.utilities import AppController, app_list
from display import DisplayDriver



class HomeController:

    def __init__(self, display: DisplayDriver, event_dispatcher: EventDispatcher, exit_callback: Callable[[], None]):
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.exit_callback: Callable[[], None] = exit_callback
        self.event_uuids: list[uuid.UUID] = []
        
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.FORWARD, self.forward)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.BACKWARD, self.backward)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.UP, self.up)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.DOWN, self.down)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.ENTER, self.enter)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.QUIT, self.quit)))

        self.app_list = app_list
        
    def forward(self, data: dict):
        logging.info("HomeScreen received forward event")
        # Handle forward event, e.g., navigate to the next screen
    def backward(self, data: dict):
        logging.info("HomeScreen received backward event")
        # Handle backward event, e.g., navigate to the previous screen
    def up(self, data: dict):
        logging.info("HomeScreen received up event")
        # Handle up event, e.g., scroll up
    def down(self, data: dict):
        logging.info("HomeScreen received down event")
        # Handle down event, e.g., scroll down
    def enter(self, data: dict):
        logging.info("HomeScreen received enter event")
        # Handle enter event, e.g., select an item
    def quit(self, data: dict):
        logging.info("HomeScreen received quit event")
        for handler_id in self.event_uuids:
            self.event_dispatcher.unregister_handler(handler_id)
        self.exit_callback()

    def draw(self):
        # Render the home screen, e.g., display a list of apps
        pass