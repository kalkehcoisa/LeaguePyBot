import asyncio
import time
from threading import Lock
from typing import Generator

from psutil import Process, process_iter, NoSuchProcess, ZombieProcess

from ...logger import get_logger, Colors

logger = get_logger("LPBv2.Lockfile")


class Lockfile:
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

    def __init__(self):
        self.lcu_pid: int
        self.pid: int
        self.port: int
        self.auth_key: str
        self.installation_path: str
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.get_lockfile)

    def get_lockfile(self):
        process = next(self.return_ux_process(), None)
        while not process:
            process = next(self.return_ux_process(), None)
            logger.debug("Process not found, start the client")
            time.sleep(1)
        process_args = self.parse_cmdline_args(process.cmdline())
        self.lcu_pid = process.pid
        self.pid = int(process_args["app-pid"])
        self.port = int(process_args["app-port"])
        self.auth_key = process_args["remoting-auth-token"]
        self.installation_path = process_args["install-directory"]
        self.print_lockfile_info()

    def return_ux_process(self) -> Generator[Process, None, None]:
        for process in process_iter():
            try:
                if process.name() in ["LeagueClientUx.exe", "LeagueClientUx"]:
                    yield process
            except NoSuchProcess:
                continue
            except ZombieProcess:
                continue

    def parse_cmdline_args(self, cmdline_args) -> dict[str, str]:
        cmds_parsed = {}
        for cmd in cmdline_args:
            if len(cmd) > 0 and cmd.startswith('--') and '=' in cmd:
                key, value = cmd[2:].split('=', 1)
                cmds_parsed[key] = value
        return cmds_parsed

    def print_lockfile_info(self):
        logger.info(
            f"auth_key: {Colors.cyan}{self.auth_key}{Colors.reset}, port: {Colors.cyan}{self.port}{Colors.reset}"
        )
