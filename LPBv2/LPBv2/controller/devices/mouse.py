from time import sleep
from threading import Lock

from pynput.mouse import Button, Controller


class Mouse:
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
        self.mouse = Controller()
        self.sleep = sleep

    def get_position(self):
        sleep(self.sleep)
        return self.mouse.position

    def set_position(self, x: int, y: int):
        sleep(self.sleep)
        self.mouse.position = (x, y)

    def left_click(self):
        sleep(self.sleep)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def right_click(self):
        sleep(self.sleep)
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)

    def set_position_and_left_click(self, x: int, y: int):
        self.set_position(x, y)
        self.left_click()

    def set_position_and_right_click(self, x: int, y: int):
        self.set_position(x, y)
        self.right_click()
