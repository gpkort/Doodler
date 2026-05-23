from collections.abc import Callable
import os
from typing_extensions import OrderedDict
import uuid
import logging

from PIL import Image, ImageDraw, ImageFont

import UI
from input import EventDispatcher, Event, EventHandler
from display import  (DisplayDriver, 
                      fontmanager,
                      FontSize, 
                     ButtonInfo, 
                     ButtonInputHandler)

APPLICATIONS: dict[str, type] = {
    "E-Reader": UI.EReaderController,
    "Audio Player": UI.PlayerController,
    "Audiobook": UI.AudioBookController,
    "Settings": UI.SettingsController
}

class AppManager:

    def __init__(self, display: DisplayDriver,  event_dispatcher: EventDispatcher, exit_callback: Callable[[], None]):
        self.display: DisplayDriver = display
        self.font_manager = fontmanager
        self.event_dispatcher = event_dispatcher
        self.current_app = None
        self.exit_callback = exit_callback
        self.event_uuids: list[uuid.UUID] = []

        self.event_uuids.append(event_dispatcher.register_handler(EventHandler(Event.QUIT, self.quit)))

    def quit(self, data: dict):
        logging.info("HomeScreen received quit event")
        for handler_id in self.event_uuids:
            self.event_dispatcher.unregister_handler(handler_id)
        self.exit_callback()

    def launch_application(self, app:UI.AppController)->None:
        ...
    def close_current_application(self, app:UI.AppController)->None:
        ...

    def draw_header(self, title:str)->None:
        ...

    def make_base_image(self, width:int = 480, height:int = 800) -> None:
        # Create and return the image to be displayed on the home screen
        top:int = 5
        r_margin:int = 470
        l_margin:int = 10
        font = self.font_manager.get_font(FontSize.LARGE) or ImageFont.load_default()

        names:dict[str, str] = {"Home": "assets/thumbnails/normal/home_n.png", 
                                "Audio Books": "assets/thumbnails/normal/audio_n.png", 
                                "MP3": "assets/thumbnails/normal/mp3_n.png", 
                                "Settings": "assets/thumbnails/normal/settings_n.png"}
        
        for name, path in names.items():
            icon:Image.Image = Image.open(path)
            icon = icon.resize((36, 36))
            icon_width, icon_height = icon.size
            print(f"Icon size: {icon_width}x{icon_height}")            
            Himage = Image.new('1', (width, height), 255)
            draw = ImageDraw.Draw(Himage)
        
            #Header
            title:str = name
            tleft, ttop, tright, tbottom = font.getbbox(title)
            tx:int = icon_width + 40 + l_margin
            ty:int = (int)(top + (icon_height - (tbottom - ttop)) // 2)
            line_y:int = (int)(max(icon_height, ttop - top)) + 15
            Himage.paste(icon, (l_margin, top))
            draw.text((tx, ty), f"{title}", font = font, fill = "black", width=2  ) #120
            draw.line((l_margin, line_y, r_margin, line_y), fill = 0) # y=45

            print(f"Header text position: ({tx}, {ty}), line_y: {line_y}")

            save_path = os.path.join("assets", "screens", "base",f"{name.lower()}_basescreen.png")
            Himage.save(save_path, "PNG")
            self.exit_callback()
            
            # self.display.initialize()
            # self.display.clear()    
            # self.display.display_image(Himage)