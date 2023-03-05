
import functools
import inspect
import logging

from config import CONFIG


class Colors:
    blue = '\033[94m'
    cyan = '\033[96m'
    light_blue = '\x1b[1;34m'
    green = '\033[92m'
    warning = '\033[93m'
    grey = '\x1b[37m'
    dark_grey = '\x1b[1;30m'
    yellow = '\x1b[1;33m'
    red = '\x1b[1;31m'
    bold_red = '\x1b[31m'
    reset = '\x1b[0m'


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    timestamp = f'{Colors.dark_grey}%(asctime)s{Colors.reset} - '
    name = f'{Colors.green}%(name)s{Colors.reset} - '
    levelname = f'%(levelname)s{Colors.reset} - '
    message = f'%(message)s'

    before = timestamp + name
    after = message + Colors.reset

    FORMATS = {
        logging.DEBUG: before + Colors.dark_grey + levelname + Colors.dark_grey + after,
        logging.INFO: before + Colors.light_blue + levelname + Colors.reset + after,
        logging.WARNING: before + Colors.yellow + levelname + Colors.yellow + after,
        logging.ERROR: before + Colors.red + levelname + Colors.red + after,
        logging.CRITICAL: before + Colors.bold_red + levelname + Colors.bold_red + after,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name='loldroid', log_to_file=True):
    logger = logging.getLogger(name)

    # Removing duplicate handlers when instanciating the logger in multiple files
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.propagate = False

    if log_to_file:
        logfile = f'{CONFIG.LOGS_FOLDER}/{name}.log'

        # Logging to a file
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)
        simpleFormatter = logging.Formatter(
            f'%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'
        )

        fh.setFormatter(simpleFormatter)
        logger.addHandler(fh)

    # Logging to console with color
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    return logger


def debug_coro(logger):
    def wrapper(func):
        @functools.wraps(func)
        async def add_exception(*args, **kwargs):
            frame = inspect.currentframe().f_back
            filename = frame.f_code.co_filename

            logger.debug(f'Running {func.__name__} from {filename}:{frame.f_lineno}')
            try:
                coro = func(*args, **kwargs)
                return await coro
            except Exception as e:
                logger.error(f'In {Colors.cyan}{func.__name__}{Colors.reset}: {e}')

        return add_exception
    return wrapper
