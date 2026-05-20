from multiprocessing import Event
from collections.abc import Callable
from typing_extensions import OrderedDict
import uuid
import logging

from PIL import Image, ImageDraw, ImageFont

from input import EventDispatcher, Event, EventHandler
import UI
from display import DisplayDriver, fontmanager 



class HomeController:

    def __init__(self, display: DisplayDriver, 
                 event_dispatcher: EventDispatcher, 
                 exit_callback: Callable[[], None]):
        
        print(f"Is font manager initialized? {fontmanager.isInitialized()}")
        self.display: DisplayDriver = display
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.exit_callback: Callable[[], None] = exit_callback
        self.event_uuids: list[uuid.UUID] = []
        
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.FORWARD, self.forward)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.BACKWARD, self.backward)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.UP, self.up)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.DOWN, self.down)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.ENTER, self.enter)))
        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.QUIT, self.quit)))

        self.app_list : OrderedDict[type, None] =  OrderedDict.fromkeys([ UI.EReaderController, UI.PlayerController, 
                                               UI.AudioBookController, 
                                               UI.SettingsController])
        self.current_selection_index: int = 0
        
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
        self.display.initialize()
        self.display.clear()

    def getHomeImage(self) -> Image.Image:
        # Create and return the image to be displayed on the home screen
        Himage = Image.new('1', (480, 800), 255)

        eread = Image.open('assets/thumbnails/ereader_tn.png')
        audi = Image.open('assets/thumbnails/audio_tn.png')
        Himage.paste(eread, (50, 50))
        Himage.paste(audi, (150, 50))
        # Himage.show()
        return Himage

    # draw = ImageDraw.Draw(Himage)
    # draw.text((10, 0), 'Doodler', font = font35, fill = 0)
    # draw.line((10, 20, 470, 20), fill = 0)
    # display.display_image(Himage)
        