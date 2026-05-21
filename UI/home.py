from multiprocessing import Event
from collections.abc import Callable
import os

from typing_extensions import OrderedDict
import uuid
import logging


from PIL import Image, ImageDraw, ImageFont, ImageFilter

from input import EventDispatcher, Event, EventHandler
import UI
from display import  (DisplayDriver, 
                      fontmanager, 
                     ButtonInfo, ButtonInputHandler)

HOME_SCREEN_PATH = os.path.join("assets", "screens", "home_screen.png")

HOME_SCREEN_ICONS:list[list[ButtonInfo]] = [
    [
    ButtonInfo(unselected_file_path="assets/thumbnails/normal/ereader_n.png",
                selected_file_path="assets/thumbnails/chosen/ereader_c.png",
                x=10, y=80, width=74, height=74),
    ButtonInfo(unselected_file_path="assets/thumbnails/normal/audio_n.png",
                selected_file_path="assets/thumbnails/chosen/audio_c.png",
                x=105, y=80, width=74, height=74),
    ButtonInfo(unselected_file_path="assets/thumbnails/normal/mp3_n.png",
                selected_file_path="assets/thumbnails/chosen/mp3_c.png",
                x=200, y=80, width=74, height=74),
    ButtonInfo(unselected_file_path="assets/thumbnails/normal/settings_n.png",
                selected_file_path="assets/thumbnails/chosen/settings_c.png",
                x=295, y=80, width=74, height=74)   
    ] 
]

class HomeController:

    def __init__(self, display: DisplayDriver, event_dispatcher: EventDispatcher, exit_callback: Callable[[], None]):
        
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
        self.button_input_handler: ButtonInputHandler = ButtonInputHandler(HOME_SCREEN_ICONS)

        self.draw_image_from_path(HOME_SCREEN_PATH)
        
    def forward(self, data: dict):
        logging.info("HomeScreen received forward event")
        bi: ButtonInfo = self.button_input_handler.direction_change(ButtonInputHandler.Direction.RIGHT)
        self.draw(self.get_selection_image(bi))
    def backward(self, data: dict):
        logging.info("HomeScreen received backward event")
        bi: ButtonInfo = self.button_input_handler.direction_change(ButtonInputHandler.Direction.LEFT)
        self.draw(self.get_selection_image(bi))           
    def up(self, data: dict):
        logging.info("HomeScreen received up event")
        bi: ButtonInfo = self.button_input_handler.direction_change(ButtonInputHandler.Direction.UP)
        self.draw(self.get_selection_image(bi))
    def down(self, data: dict):
        logging.info("HomeScreen received down event")
        bi: ButtonInfo = self.button_input_handler.direction_change(ButtonInputHandler.Direction.DOWN)
        self.draw(self.get_selection_image(bi))
    def enter(self, data: dict):
        logging.info("HomeScreen received enter event")
        # Handle enter event, e.g., select an item
    def quit(self, data: dict):
        logging.info("HomeScreen received quit event")
        for handler_id in self.event_uuids:
            self.event_dispatcher.unregister_handler(handler_id)
        self.exit_callback()

    def draw(self, image: Image.Image ):
        # Render the home screen, e.g., display a list of apps
        self.display.initialize()
        self.display.clear()
        self.display.display_image(image)

    def draw_image_from_path(self, path:str):
        if os.path.exists(path):
            im:Image.Image = Image.open(path)
            self.draw(im)

    def get_selection_image(self, button: ButtonInfo) -> Image.Image:
        # Draw a selection box around the currently selected item        
        top_image: Image.Image = Image.open(HOME_SCREEN_PATH)
        select: Image.Image = Image.open(button.selected_file_path)
        top_image.paste(select, (button.x, button.y))
        return top_image
       
    # def getHomeImage(self) -> Image.Image:
    #     # Create and return the image to be displayed on the home screen
    #     top:int = 5
    #     r_margin:int = 10
    #     l_margin:int = 470
    #     first_row_y:int = 80
        
    #     Himage = Image.new('1', (480, 800), 255)
    #     draw = ImageDraw.Draw(Himage)
        
    #     #Header
    #     draw.text((150, top), 'HOME', font = fontmanager.get_font(FontSize.LARGE), fill = 0)
    #     draw.line((l_margin, top + 45, 470, top + 45), fill = 0)
       
    #     for key, value in HomeScreenIcons.items():
    #        icon = Image.open(value.unselected_file_path)
    #        Himage.paste(icon, (value.x, value.y))

    #     #Himage.save(os.path.join("assets", "screens", "home_screen.png"), "PNG")
    #     return Himage

    
        