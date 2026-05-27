from collections.abc import Callable
import os
from typing import Any
from typing_extensions import OrderedDict
import uuid
import logging

from PIL import Image
import UI
from input import EventDispatcher
from display import  DisplayDriver, fontmanager
from UI import IconInfo, IconInputHandler, AppController


BASE_SCREEN_PATH = "assets/screens/base/home_basescreen.png"

APPLICATIONS: dict[str, UI.AppInfo] = {
    "EReader":UI.AppInfo(UI.EReaderController, "assets/screens/base/e-reader_basescreen.png"), 
    "Player":UI.AppInfo(UI.PlayerController, "assets/screens/base/mp3_basescreen.png"), 
    "AudioBook":UI.AppInfo(UI.AudioBookController, "assets/screens/base/audiobook_basescreen.png"), 
    "Settings":UI.AppInfo(UI.SettingsController, "assets/screens/base/settings_basescreen.png") 
}

HOME_SCREEN_ICONS:list[list[IconInfo]] = [
    [
    IconInfo(name="EReader",
                icon_path="assets/thumbnails/chosen/ereader_c.png"),
    IconInfo(name="Player",
                icon_path="assets/thumbnails/chosen/audio_c.png"),
    IconInfo(name="AudioBook",
                icon_path="assets/thumbnails/chosen/mp3_c.png"),
    IconInfo(name="Settings",
                icon_path="assets/thumbnails/chosen/settings_c.png")   
    ]
]

class AppManager(AppController):

    def __init__(self, display: DisplayDriver,  event_dispatcher: EventDispatcher, exit_callback: Callable[[], None]):
        super().__init__(display, event_dispatcher, exit_callback, home_screen_image=Image.open(BASE_SCREEN_PATH))

        self.font_manager = fontmanager
        self.current_app = None
        self.current_app: UI.AppController | None = None

        self.register_app_controller()
        self.icon_input_handler: IconInputHandler = IconInputHandler(display, 
                                                                     HOME_SCREEN_ICONS,
                                                                     Image.open(BASE_SCREEN_PATH))
        
        

    
    def handle_event(self, event: dict):
        self.logger.info("AppManager received event: %s", event)
        
    
    def forward(self, data: dict):
        self.logger.info("AppManager received forward event")
        self.event_dispatcher.unregister_all_handlers()
        self.exit_callback()
        
    
    def backward(self, data: dict):
        self.logger.info("AppManager received backward event")
    
    def up(self, data: dict):
        self.logger.info("AppManager received up event")
        self.icon_input_handler.direction_change(IconInputHandler.Direction.UP)
    
    def down(self, data: dict):
        self.logger.info("AppManager received down event")
        self.icon_input_handler.direction_change(IconInputHandler.Direction.DOWN)
    
    def right(self, data: dict):
        self.logger.info("AppManager received right event")
        self.icon_input_handler.direction_change(IconInputHandler.Direction.RIGHT)
    
    def left(self, data: dict):
        self.logger.info("AppManager received left event")
        self.icon_input_handler.direction_change(IconInputHandler.Direction.LEFT)
    
    def enter(self, data: dict):
        self.logger.info("AppManager received enter event")

        if self.icon_input_handler.current_button is not None:
            app_name = self.icon_input_handler.current_button.name
            app_info = APPLICATIONS.get(app_name)
            if app_info:
                self.launch_application(app_name, app_info)
            else:
                self.logger.warning("No application found for name: %s", app_name)
    
    
    def quit(self, data : dict[Any, Any]):
        logging.info("HomeScreen received quit event")
        self.event_dispatcher.unregister_all_handlers()
        self.exit_callback()

    def launch_application(self, name:str, app:UI.AppInfo)->None:
        self.logger.info("Launching application: %s", name)
        img: Image.Image = Image.open(app.base_image_path)
        self.current_app = app.app_class(self.display, 
                                         self.event_dispatcher, 
                                         self.exit_callback,
                                         home_screen_image=img) # type: ignore
        
       
        
    def close_current_application(self, app:UI.AppController)->None:
        ...
    def handle_launch_event(self, app_name:str)->None:
        ...
    def draw_header(self, title:str)->None:
        ...

    