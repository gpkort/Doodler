from typing import Callable

import UI
from display.display_driver import DisplayDriver
from input.dispatcher import EventDispatcher

class EReaderController(UI.AppController):
    def __init__(self, display: DisplayDriver, event_dispatcher: EventDispatcher, exit_callback: Callable[[], None]):
        super().__init__(display, event_dispatcher, exit_callback)

    @staticmethod
    def get_name() -> str:
        return "E-Reader"

    def handle_event(self, event: dict):
        pass