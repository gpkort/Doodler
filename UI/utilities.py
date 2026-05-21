from abc import ABC, abstractmethod

class AppController(ABC):
    @staticmethod
    def get_name() -> str:
        return "BaseApp"
    
    @abstractmethod
    def handle_event(self, event: dict):
        pass



