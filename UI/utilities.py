from abc import ABC, abstractmethod
from collections import OrderedDict

# from UI.player import PlayerController
# from UI.audiobook import AudioBookController
# from UI.settings import SettingsController
# from UI.e_reader import EReaderController

class AppController(ABC):
    @abstractmethod
    @staticmethod
    def get_name() -> str:
        pass
    
    @abstractmethod
    def handle_event(self, event: dict):
        pass



current_app = None