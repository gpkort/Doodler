import UI

class SettingsController(UI.AppController):
    def __init__(self,):
        super().__init__()

    @staticmethod
    def get_name() -> str:
        return "Settings"

    def handle_event(self, event: dict):
        pass