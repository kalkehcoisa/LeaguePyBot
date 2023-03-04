from time import sleep
from threading import Lock
import os


class Keyboard:
    __instance = None
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls.__instance is None:
                instance = super().__call__(*args, **kwargs)
                cls.__instance = instance
        return cls.__instance

    def __init__(self, sleep=0):
        if os.name == "nt":
            from .keyboard_pydirectinput import KeyboardPyDirectInput
            self.keyboard = KeyboardPyDirectInput()
        else:
            from .keyboard_pynput import KeyboardPynput
            self.keyboard = KeyboardPynput()
        self.sleep = sleep

    def input_key(self, key):
        sleep(self.sleep)
        self.keyboard.input_key(key)

    def input_word(self, word: str):
        sleep(self.sleep)
        self.keyboard.input_word(word)

    def esc(self):
        sleep(self.sleep)
        self.keyboard.esc()

    def enter(self):
        sleep(self.sleep)
        self.keyboard.enter()

    def space(self):
        sleep(self.sleep)
        self.keyboard.space()
