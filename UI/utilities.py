from abc import ABC, abstractmethod
from collections import OrderedDict

class AppController(ABC):
    @staticmethod
    def get_name() -> str:
        return "BaseApp"
    
    @abstractmethod
    def handle_event(self, event: dict):
        pass



current_app = None