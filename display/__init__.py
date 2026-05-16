# Define the __all__ variable
__all__ = ["display", "web_display", "local_display"]

# Import the submodules
from . import display
from . import web_display
from . import local_display