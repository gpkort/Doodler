from collections.abc import Callable
import os
from typing import Any
from typing_extensions import OrderedDict
import uuid
import logging

from PIL import Image, ImageDraw, ImageFont

import UI
from input import EventDispatcher, Event, EventHandler
from display import  DisplayDriver, fontmanager

APPLICATIONS: dict[str, UI.AppInfo] = {
    "Home":UI.AppInfo(UI.HomeController, "assets/screens/base/home_basescreen.png"), 
    "EReader":UI.AppInfo(UI.EReaderController, "assets/screens/base/e-reader_basescreen.png"), 
    "Player":UI.AppInfo(UI.PlayerController, "assets/screens/base/mp3_basescreen.png"), 
    "AudioBook":UI.AppInfo(UI.AudioBookController, "assets/screens/base/audiobook_basescreen.png"), 
    "Settings":UI.AppInfo(UI.SettingsController, "assets/screens/base/settings_basescreen.png") 
}

class AppManager:

    def __init__(self, display: DisplayDriver,  event_dispatcher: EventDispatcher, exit_callback: Callable[[], None]):
        self.display: DisplayDriver = display
        self.font_manager = fontmanager
        self.event_dispatcher = event_dispatcher
        self.current_app = None
        self.exit_callback = exit_callback
        self.event_uuids: list[uuid.UUID] = []
        self.logger = logging.getLogger("AppManager")
        self.current_app: UI.AppController | None = None

        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.QUIT, self.quit)))
        self.launch_application("Home", APPLICATIONS["Home"])

    def quit(self, data : dict[Any, Any]):
        logging.info("HomeScreen received quit event")
        for handler_id in self.event_uuids:
            self.event_dispatcher.unregister_handler(handler_id)
        self.exit_callback()

    def launch_application(self, name:str, app:UI.AppInfo)->None:
        self.logger.info("Launching application: %s", name)
        img: Image.Image = Image.open(app.base_image_path)
        self.current_app = app.app_class(self.display, 
                                         self.event_dispatcher, 
                                         self.exit_callback,
                                         home_screen_image=img) # type: ignore
        
        if isinstance(self.current_app, UI.HomeController):
            self.current_app.register_launch_event(self.handle_launch_event) # type: ignore
        
    def close_current_application(self, app:UI.AppController)->None:
        ...
    def handle_launch_event(self, app_name:str)->None:
        ...
    def draw_header(self, title:str)->None:
        ...

    