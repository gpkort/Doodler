from pynput import keyboard
from input import Event, EventDispatcher

class KeyboardInputHandler(EventDispatcher):
    def __init__(self):
        super().__init__()
        print("Initializing KeyboardInputHandler")
        self.listener = keyboard.Listener( on_release=self.on_release) #, suppress=True)
        self.listener.start()   
    
    def on_release(self, key):
        print(f"Key released: {key}")
        event: Event = Event.UNKNOWN
        if key == keyboard.Key.left:
            super()._dispatch(Event.BACKWARD)
        if key == keyboard.Key.right:
            super()._dispatch(Event.FORWARD)   
        if key == keyboard.Key.down:
            super()._dispatch(Event.DOWN)
        if key == keyboard.Key.up:
            super()._dispatch(Event.UP)
        if key == keyboard.Key.esc:
            super()._dispatch(Event.QUIT)
        if key == keyboard.Key.enter:
            super()._dispatch(Event.ENTER)
            
        try:        
            super()._dispatch(event)
        except AttributeError:
            super()._dispatch(Event.UNKNOWN)
    
   
    
