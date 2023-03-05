
from time import sleep
from threading import Lock
import os
import signal
import threading

import keyboard
import pydirectinput
from pynput.keyboard import Controller, Key, Listener
from pynput.mouse import Button, Controller

from logger import get_logger

pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0.01

logger = get_logger("loldroid.Devices")


class KeyboardPyKeyboard:
    def __init__(self):
        pass

    def input_key(self, key: str):
        special = None
        if "Shift" in key:
            special = 'Shift'
        elif "Ctrl" in key:
            special = 'Ctrl'
        elif "Alt" in key:
            special = 'Alt'

        if special:
            keyboard.press(special.lower())
            keyboard.press(key.replace(special, ""))
            keyboard.release(special.lower())
        else:
            pydirectinput.press(key)

    def input_word(self, word: str):
        logger.debug(word)
        keyboard.write(word.lower())

    def esc(self):
        pydirectinput.press("esc")

    def enter(self):
        pydirectinput.press("enter")

    def space(self):
        pydirectinput.press("space")


class KeyboardPynput:
    def __init__(self):
        self.keyboard = Controller()

    def input_key(self, key):
        print(key)
        if "Shift" in key:
            with self.keyboard.pressed(Key.shift):
                self.keyboard.tap(key.replace("Shift", ""))
        elif "Ctrl" in key:
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.tap(key.replace("Ctrl", ""))
        elif "Alt" in key:
            with self.keyboard.pressed(Key.alt):
                self.keyboard.tap(key.replace("Alt", ""))
        else:
            self.keyboard.tap(key)

    def input_word(self, word: str):
        self.keyboard.type(word)

    def esc(self):
        self.keyboard.tap(Key.esc)

    def enter(self):
        self.keyboard.tap(Key.enter)

    def space(self):
        self.keyboard.tap(Key.space)


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
            self.keyboard = KeyboardPyKeyboard()
        else:
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


class KeyboardListener:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press)
        threading.Thread(target=self.listen).start()

    def listen(self):
        with self.listener as listener:
            listener.join()

    def on_press(self, key):
        if key == Key.end:
            pid = int(os.getpid())
            try:
                os.kill(pid, signal.SIGKILL)
            except:
                os.system(f"taskkill /f /pid {pid}")
            return False


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
