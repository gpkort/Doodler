import asyncio
from websockets.asyncio.client import connect
from dataclasses import dataclass
from typing import Any

from display.display import Display

@dataclass
class DisplayMessage:
    command: str
    data: dict[str, Any] 

class WebDisplay(Display):
    def __init__(self, display_width: int, display_height: int, ip_address: str, port: int):
        super().__init__(display_width, display_height)
        self.ip_address = ip_address
        self.port = port
        self.isConnected = False

    def init(self):
        mess:DisplayMessage = DisplayMessage(command="init", data={"width": self.display_width, "height": self.display_height})
        response = asyncio.run(self._send(str(mess)))
        if response.lower() != "ok":
            raise Exception(f"Failed to initialize display: {response}")
        self.isConnected = True
    
    def display (self, image:bytes):
        if self.isConnected:           
            mess:DisplayMessage = DisplayMessage(command="display", data={"image": image})
            response = asyncio.run(self._send(str(mess)))


    async def _send(self, message: str) -> str:
        async with connect(f"ws://{self.ip_address}:{self.port}") as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            print(response)
            return str(response)