import aiohttp
import ssl
from threading import Lock

from logger import get_logger, debug_coro

logger = get_logger("loldroid.Caller")


class Caller:
    __instance = None
    _lock: Lock = Lock()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls.__instance is None:
                instance = super().__call__(*args, **kwargs)
                cls.__instance = instance
        return cls.__instance

    def __init__(self):
        super().__init__()

    @property
    def connector(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return aiohttp.TCPConnector(ssl=context)

    @debug_coro(logger)
    async def get(self, url):
        async with aiohttp.ClientSession(headers=self.headers, connector=self.connector) as session:
            response = await session.get(url)
            response_json = await response.json()
            return response_json

    @debug_coro(logger)
    async def post(self, url, payload):
        async with aiohttp.ClientSession(headers=self.headers, connector=self.connector) as session:
            response = await session.post(
                url=url,
                json=payload,
            )
            response_json = await response.json()
            return response_json
