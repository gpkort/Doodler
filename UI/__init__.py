__all__ = ["home", "audiobook", "e_reader", "settings", "player", "utilities"]

from .home import HomeController
from .audiobook import AudioBookController
from .e_reader import EReaderController
from .settings import SettingsController
from .player import PlayerController    
from .utilities import AppController, app_list, current_app