import time
from typing import Generator

from psutil import Process, process_iter, NoSuchProcess, ZombieProcess

from exceptions import GracefulExit
from logger import get_logger, Colors

logger = get_logger('loldroid.ClientData')


class ClientData:
    """
    Stores Lol client data: pid, port, path, auth_key.
    """
    __instance = None
    lcu_pid: int
    pid: int
    port: int
    auth_key: str
    installation_path: str

    def _log(self):
        return (
            f'auth_key: {Colors.cyan}{self.auth_key}{Colors.reset}, '
            f'port: {Colors.cyan}{self.port}{Colors.reset}'
        )

    def __repr__(self):
        return f'ClientData ({self._log()})'
    __str__ = __repr__

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            cls.__instance = instance
            instance.acquire()
        return cls.__instance

    def acquire(self):
        for _ in range(10):
            process = next(self.return_ux_process(), None)
            if process:
                break
            logger.debug('Process not found, start the client')
            time.sleep(1)
        else:
            raise GracefulExit('Process not found, start the client')
        process_args = self.parse_cmdline_args(process.cmdline())
        self.lcu_pid = process.pid
        self.pid = int(process_args['app-pid'])
        self.port = int(process_args['app-port'])
        self.auth_key = process_args['remoting-auth-token']
        self.installation_path = process_args['install-directory']
        self.print_log_info()

    def return_ux_process(self) -> Generator[Process, None, None]:
        for process in process_iter():
            try:
                if process.name() in ['LeagueClientUx.exe', 'LeagueClientUx']:
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

    def print_log_info(self):
        logger.info(self._log())
