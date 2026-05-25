from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
# from UI import AppManager

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