from UI import AppController

class AudioBookController(AppController):
    def __init__(self):
        pass

    @staticmethod
    def get_name() -> str:
        return "Audio Book"

    def handle_event(self, event: dict):
        pass