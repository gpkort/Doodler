from abc import ABC, abstractmethod
from collections import OrderedDict

from UI import (HomeController, 
                SettingsController, 
                PlayerController, 
                AudioBookController, 
                EReaderController)

class AppController(ABC):
    @abstractmethod
    @staticmethod
    def get_name() -> str:
        pass
    
    @abstractmethod
    def handle_event(self, event: dict):
        pass

app_list =  OrderedDict.fromkeys([EReaderController, PlayerController, AudioBookController, SettingsController])

current_app = None