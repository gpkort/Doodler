from UI import AppController

class EReaderController(AppController):
    def __init__(self):
        pass

    @staticmethod
    def get_name() -> str:
        return "E-Reader"

    def handle_event(self, event: dict):
        pass