import UI

class EReaderController(UI.AppController):
    def __init__(self):
        pass

    @staticmethod
    def get_name() -> str:
        return "E-Reader"

    def handle_event(self, event: dict):
        pass