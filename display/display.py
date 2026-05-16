from dataclasses import dataclass

@dataclass
class PinConfig:
    reset_pin: int | str | None
    dc_pin: int | str | None
    cs_pin: int | str | None
    busy_pin: int | str | None
    power_pin: int | str | None
    mosi_pin: int | str | None
    sck_pin: int | str | None
    cs_pin: int | str | None

class Display:
    def __init__(self, display_width: int, display_height: int, pin_config: PinConfig| None = None):
        self.display_width = display_width
        self.display_height = display_height
        self.pin_config = pin_config

    def reset (self):
        print("NOT IMPLEMENTED: reset")
    def init (self):
        print("NOT IMPLEMENTED: init")
    def init_fast (self):
        print("NOT IMPLEMENTED: init_fast") 
    def display (self, image:bytes):
        print("NOT IMPLEMENTED: display")
    def init_4Gray (self):
        print("NOT IMPLEMENTED: init_4Gray")    
    def display_Partial(self, image):
        print("NOT IMPLEMENTED: display_Partial")
    def display_4Gray(self, image):
        print("NOT IMPLEMENTED: display_4Gray")
    def Clear(self):
        print("NOT IMPLEMENTED: Clear")
    def sleep(self):
        print("NOT IMPLEMENTED: sleep")