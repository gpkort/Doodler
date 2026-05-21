"""
E-ink display driver abstraction for Waveshare 7.5" e-Paper HAT.
PORTABILITY: 100% portable - SPI interface identical on Pi 3B+ and Pi Zero 2 W
"""

import sys
import os
from typing import Any
from PIL import Image, ImageTk
import logging
import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

# Add Waveshare library to path
LIB_PATH = os.path.join(os.path.dirname(__file__), '../lib')
if os.path.exists(LIB_PATH):
    sys.path.insert(0, LIB_PATH)

@dataclass
class ButtonInfo:
    unselected_file_path: str
    selected_file_path: str
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

class ButtonInputHandler:
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self, buttons: list[list[ButtonInfo]], row_index: int = -1, column_index: int = -1):
        self.buttons = buttons
        self.row_index = row_index
        self.column_index = column_index

    @property
    def current_button(self) -> ButtonInfo | None:
        if self.row_index == -1 or self.column_index == -1:
            return None
        return self.buttons[self.row_index][self.column_index]
    
    @property
    def current_row_index(self) -> int:
        return self.row_index
    @property
    def current_column_index(self) -> int:
        return self.column_index

    def direction_change(self, direction: Direction) -> ButtonInfo :
        if self.row_index == -1 or self.column_index == -1:
            self.row_index = 0
            self.column_index = 0
            return self.buttons[self.row_index][self.column_index]
    
        if direction == ButtonInputHandler.Direction.UP:
            self.row_index = self.row_index - 1 if self.row_index > 0 else len(self.buttons) - 1
        elif direction == ButtonInputHandler.Direction.DOWN:
            self.row_index = self.row_index + 1 if self.row_index < len(self.buttons) - 1 else 0
        elif direction == ButtonInputHandler.Direction.LEFT:
            self.column_index = self.column_index - 1 if self.column_index > 0 else len(self.buttons[self.row_index]) - 1
        elif direction == ButtonInputHandler.Direction.RIGHT:
            self.column_index = self.column_index + 1 if self.column_index < len(self.buttons[self.row_index]) - 1 else 0

        return self.buttons[self.row_index][self.column_index]
        
   
class DisplayDriver(ABC):
    """Abstract base class for display"""
    
    @abstractmethod
    def initialize(self)->None:
        pass
    
    @abstractmethod
    def clear(self)->None:
        pass
    
    @abstractmethod
    def display_image(self, image: Image.Image, use_partial: bool = True, skip_counter: bool = False)->None:
        pass
    
    @abstractmethod
    def sleep(self)->None:
        pass
    
    @abstractmethod
    def cleanup(self)->None:
        pass



class EPaperDisplayDriver(DisplayDriver):
    """
    Hardware abstraction for Waveshare 7.5" e-Paper HAT (800x480)
    """

    def __init__(self, width: int = 800, height: int = 480, rotation: int = 0, use_local: bool = False):
        """
        Initialize display driver

        Args:
            width: Display width in pixels (logical, after rotation)
            height: Display height in pixels (logical, after rotation)
            rotation: Rotation angle (0, 90, 180, 270)
            use_local: Whether to use local library path for Waveshare driver
        """
        self.width = width
        self.height = height
        self.rotation = rotation
        self.epd = None
        self.logger = logging.getLogger(__name__)
        self.partial_refresh_count = 0
        self.full_refresh_interval = 5  # Full refresh every N page turns
        self.first_display = True  # Force full refresh on first display

        # Physical hardware dimensions (always 800x480 for this display)
        self.hw_width = 800
        self.hw_height = 480

        # Track if partial refresh mode has been initialized
        self.partial_mode_initialized = False
        
        # Grayscale mode support - 4-bit grayscale for smooth anti-aliased text
        # DISABLED: Too slow (no partial refresh support) and didn't improve text quality
        self.use_grayscale = False  # Disabled - use 1-bit mode with partial refresh
        self.grayscale_initialized = False

        # Try to import Waveshare library
        if not use_local:
            try:
                from lib import epd7in5_V2
                self.epd_module = epd7in5_V2
                self.hardware_available = True
                self.logger.info("Using Waveshare 7.5inch V2 driver (800x480, 4-gray mode)")
            except ImportError:
                self.logger.warning("Waveshare V2 library not found. Running in mock mode.")
                self.hardware_available = False
        else:
            self.hardware_available = False
            
    def initialize(self):
        """Initialize the display hardware"""
        if not self.hardware_available:
            self.logger.info("Mock display initialized (no hardware)")
            return

        try:
            self.epd = self.epd_module.EPD()
            self.epd.init()
            self.logger.info("E-ink display initialized successfully")
        except Exception as e:
            self.logger.error(f"Display initialization failed: {e}")
            raise

    def clear(self):
        """Clear the display to white"""
        if not self.hardware_available or not self.epd:
            self.logger.debug("Mock clear")
            return

        try:
            self.epd.Clear()
            self.logger.info("Display cleared")
        except Exception as e:
            self.logger.error(f"Display clear failed: {e}")

    def display_image(self, image: Image.Image, use_partial: bool = True, skip_counter: bool = False):
        """
        Display a PIL Image on the screen with partial or full refresh

        Args:
            image: PIL Image object (will be resized and rotated as needed)
            use_partial: Whether to use partial refresh (if False, forces full refresh)
            skip_counter: If True, bypass periodic full refresh counter (for non-reader screens)
        """
        # Ensure image is correct size
        # NOTE: If this resize happens, there's a bug in the renderer - it should produce
        # images at exactly the right size
        if image.size != (self.width, self.height):
            self.logger.warning(f"UNEXPECTED RESIZE from {image.size} to ({self.width}, {self.height}) - check renderer!")
            # Use NEAREST for 1-bit images to avoid creating gray pixels
            # LANCZOS for grayscale/color for smooth scaling
            if image.mode == '1':
                image = image.resize((self.width, self.height), Image.Resampling.NEAREST)
            else:
                image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)

        # For grayscale mode, keep the image as grayscale (mode 'L')
        # Only convert to 1-bit if NOT using grayscale mode
        if not self.use_grayscale:
            if image.mode != '1':
                self.logger.debug(f"Converting image from {image.mode} to 1-bit (grayscale mode disabled)")
                image = image.convert('1', dither=Image.Dither.NONE)
        else:
            # For grayscale mode, ensure image is 'L' (8-bit grayscale)
            if image.mode == '1':
                image = image.convert('L')

        # Apply rotation if needed (for portrait mode)
        if self.rotation != 0:
            # Use BILINEAR for grayscale rotation (smooth), NEAREST for 1-bit (sharp)
            resample = Image.Resampling.NEAREST if image.mode == '1' else Image.Resampling.BILINEAR
            image = image.rotate(-self.rotation, expand=True, resample=resample)
            self.logger.debug(f"Rotated image by {self.rotation} degrees")

        if not self.hardware_available or not self.epd:
            # Mock mode - save image to file
            output_file = "output/display_output.png"
            os.makedirs("output", exist_ok=True)
            image.save(output_file)
            self.logger.info(f"Mock display: Image saved to {output_file}")
            return

        try:
            # In grayscale mode, always use full refresh (4Gray doesn't support partial)
            # In 1-bit mode, use partial refresh as before
            if self.use_grayscale:
                # Grayscale 4-Gray mode - always full refresh
                self.logger.info(f"Performing 4-Gray FULL refresh")
                
                # Always reinitialize 4Gray mode for clean state
                # This prevents ghosting and display corruption
                self.logger.debug("Initializing 4-Gray mode")
                self.epd.init_4Gray()
                
                # Ensure image is grayscale mode 'L'
                if image.mode != 'L':
                    image = image.convert('L')
                
                self.epd.display_4Gray(self.epd.getbuffer_4Gray(image))
                self.partial_refresh_count = 0
                self.partial_mode_initialized = False
                self.grayscale_initialized = True
            else:
                # 1-bit mode - supports partial refresh
                # Ensure image is 1-bit
                if image.mode != '1':
                    image = image.convert('1', dither=Image.Dither.NONE)
                
                # Decide whether to use partial or full refresh
                # Always do full refresh on first display to clear any ghosting from previous session
                # If skip_counter is True, ignore the periodic refresh counter (for non-reader screens)
                should_full_refresh = self.first_display or not use_partial or (not skip_counter and self.partial_refresh_count >= self.full_refresh_interval)

                if should_full_refresh:
                    # Full refresh - clears ghosting
                    if self.first_display:
                        self.logger.info(f"Performing FIRST FULL refresh (clearing any previous ghosting)")
                    else:
                        self.logger.info(f"Performing FULL refresh (count reset from {self.partial_refresh_count})")

                    # Reinitialize for full refresh if we were in partial mode
                    if self.partial_mode_initialized:
                        self.logger.info("Reinitializing display for full refresh mode")
                        self.epd.init()
                        self.partial_mode_initialized = False

                    self.epd.display(self.epd.getbuffer(image))
                    self.partial_refresh_count = 0
                    self.first_display = False  # Clear first display flag after full refresh
                else:
                    # Partial refresh - faster but may cause ghosting
                    buffer_data = self.epd.getbuffer(image)

                    # Waveshare 7.5" V2 uses display_Partial(Image, Xstart, Ystart, Xend, Yend)
                    if hasattr(self.epd, 'display_Partial'):
                        try:
                            # Initialize partial refresh mode if not already done
                            if not self.partial_mode_initialized and hasattr(self.epd, 'init_part'):
                                self.logger.info("Initializing partial refresh mode (init_part)")
                                self.epd.init_part()
                                self.partial_mode_initialized = True
                            
                            # Full screen partial refresh with HARDWARE coordinates (always 800x480)
                            self.epd.display_Partial(buffer_data, 0, 0, self.hw_width, self.hw_height)
                            self.partial_refresh_count += 1
                            self.logger.info(f"PARTIAL refresh {self.partial_refresh_count}/{self.full_refresh_interval}")
                        except Exception as e:
                            self.logger.warning(f"Partial refresh failed: {e}, using full refresh")
                            self.epd.display(buffer_data)
                            self.partial_refresh_count = 0
                            self.partial_mode_initialized = False
                    else:
                        # Fallback: try other method names
                        partial_method = None
                        if hasattr(self.epd, 'displayPartial'):
                            partial_method = self.epd.displayPartial
                        elif hasattr(self.epd, 'DisplayPartial'):
                            partial_method = self.epd.DisplayPartial

                        if partial_method:
                            try:
                                partial_method(buffer_data)
                                self.partial_refresh_count += 1
                                self.logger.info(f"PARTIAL refresh {self.partial_refresh_count}/{self.full_refresh_interval}")
                            except Exception as e:
                                self.logger.warning(f"Partial refresh failed: {e}, using full refresh")
                                self.epd.display(buffer_data)
                                self.partial_refresh_count = 0
                        else:
                            # Partial refresh not supported
                            self.logger.warning("Partial refresh not available on this display, using full refresh")
                            self.epd.display(buffer_data)

        except Exception as e:
            self.logger.error(f"Display image failed: {e}")
            raise

    def set_full_refresh_interval(self, interval: int):
        """
        Set how many partial refreshes before a full refresh

        Args:
            interval: Number of partial refreshes (e.g., 5 = full refresh every 5 page turns)
        """
        self.full_refresh_interval = max(1, interval)
        self.logger.info(f"Full refresh interval set to {self.full_refresh_interval}")

    def reset_partial_counter(self):
        """Reset the partial refresh counter (call when changing screens)"""
        self.partial_refresh_count = 0
        self.logger.debug("Partial refresh counter reset")

    def sleep(self):
        """Put display into low-power sleep mode"""
        if not self.hardware_available or not self.epd:
            self.logger.debug("Mock sleep")
            return

        try:
            self.epd.sleep()
            self.logger.info("Display entered sleep mode")
        except Exception as e:
            self.logger.error(f"Display sleep failed: {e}")

    def cleanup(self):
        """Clean up resources and put display to sleep"""
        if not self.hardware_available or not self.epd:
            self.logger.debug("Mock cleanup")
            return

        try:
            self.epd.sleep()
            self.logger.info("Display cleaned up")
        except Exception as e:
            self.logger.error(f"Display cleanup failed: {e}")

class TkDisplayDriver(DisplayDriver):
    """Tkinter display driver for testing without hardware"""
    
    def __init__(self, root: tk.Tk, width: int = 360, height: int = 600, rotation: int = 0):
        self.width = width
        self.height = height
        self.rotation = rotation
        self.logger = logging.getLogger(__name__)
        
        self.root = root        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.imagesprite = None  # Keep reference to PhotoImage to prevent garbage collection

    def initialize(self):
        self.logger.info("Mock display initialized")

    def clear(self):
        self.logger.info("Mock display cleared")

    def display_image(self, image: Image.Image, use_partial: bool = True, skip_counter: bool = False):
        image = image.resize((360, 600), Image.Resampling.NEAREST)
        tk_img = ImageTk.PhotoImage(image)
        self.imagesprite = tk_img
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        self.root.update_idletasks()
        self.root.update()

    def sleep(self):
        self.logger.info("Mock display sleep")

    def cleanup(self):
        self.logger.info("Mock display cleanup")

def display_factory(settings: dict[str, Any]) -> EPaperDisplayDriver:
    """
    Factory function to create a DisplayDriver instance based on settings

    Args:
        settings: Dictionary containing display settings (width, height, orientation)

    Returns:
        An instance of DisplayDriver
    """
    width = settings.get("width", 480)
    height = settings.get("height", 800)
    orientation = settings.get("orientation", 90)
    use_local = settings.get("use_local_display", True)
    return EPaperDisplayDriver(width=width, height=height, rotation=orientation, use_local=use_local)