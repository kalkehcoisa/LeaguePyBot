import os
import shutil
from threading import Lock


class Configurator:
    __instance = None
    _lock: Lock = Lock()

    LOGS_FOLDER = 'logs'

    @classmethod
    def init_system(cls):
        cfg = cls.__instance

        # empty the LOGS_FOLDER when the system is started
        if os.path.exists(cfg.LOGS_FOLDER):
            shutil.rmtree(cfg.LOGS_FOLDER)
        os.makedirs(cfg.LOGS_FOLDER)

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls.__instance is None:
                instance = super().__call__(*args, **kwargs)
                cls.__instance = instance
                cls.init_system()
        return cls.__instance

    def __init__(self):
        super().__init__()


CONFIG = Configurator()
