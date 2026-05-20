from multiprocessing import Event
from collections.abc import Callable
from typing_extensions import OrderedDict
import uuid
import logging


class AppManager:

    def __init__(self, display, font_manager, event_dispatcher):
        self.display = display
        self.font_manager = font_manager
        self.event_dispatcher = event_dispatcher
        self.current_app = None