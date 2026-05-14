
import asyncio
from websockets.asyncio.client import connect

from dataclasses import dataclass

async def Listener():
    async with connect("ws://172.16.123.70:8765") as websocket:
        await websocket.send("smello world!")
        message = await websocket.recv()
        print(message)
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
    def __init__(self):
        pass

    def reset (self):
        pass
    def init (self, image):
        pass
    def init_fast (self, image):
        pass
    def init_4Gray (self, image):
        pass    
    def display_Partial(self, image):
        pass
    def display_4Gray(self, image):
        pass
    def Clear(self, image):
        pass
    def sleep(self, image):
        ...