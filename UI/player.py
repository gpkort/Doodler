import UI

class PlayerController(UI.AppController):
    def __init__(self,):
        pass

    @staticmethod
    def get_name() -> str:
        return "Music Player"

    def handle_event(self, event: dict):
        pass