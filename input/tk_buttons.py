import tkinter as tk
from input import Event, EventDispatcher

class TkButtonInputHandler(EventDispatcher):
    def __init__(self, root: tk.Tk):
        super().__init__()
        self.root = root
        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        backward_button = tk.Button(button_frame, text="Left", command=lambda: self._dispatch(Event.LEFT))
        backward_button.grid(row=1, column=1)
        
        enter_button = tk.Button(button_frame, text="Enter", command=lambda: self._dispatch(Event.ENTER))
        enter_button.grid(row=1, column=2)

        forward_button = tk.Button(button_frame, text="Right", command=lambda: self._dispatch(Event.RIGHT))
        forward_button.grid(row=1, column=3)        

        up_button = tk.Button(button_frame, text="Up", command=lambda: self._dispatch(Event.UP))
        up_button.grid(row=0, column=2)

        down_button = tk.Button(button_frame, text="Down", command=lambda: self._dispatch(Event.DOWN))
        down_button.grid(row=2, column=2)        

        quit_button = tk.Button(button_frame, text="BK", command=lambda: self._dispatch(Event.BACKWARD))
        quit_button.grid(row=1, column=0)
        
        quit_button = tk.Button(button_frame, text="FWD", command=lambda: self._dispatch(Event.FORWARD))
        quit_button.grid(row=1, column=4)
