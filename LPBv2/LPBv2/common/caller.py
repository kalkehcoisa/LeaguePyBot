import aiohttp
import json
import ssl
from threading import Lock

from .utils import debug_coro
from ..logger import get_logger

logger = get_logger("LPBv2.Caller")


class Caller:
    __instance = None
    _lock: Lock = Lock()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

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
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.connector = aiohttp.TCPConnector(ssl=self.context)

    @debug_coro
    async def get(self, url):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector=self.connector) as session:
                response = await session.get(url)
                response_json = await response.json()
                return response_json
        except Exception as e:
            logger.error(e)

    @debug_coro
    async def post(self, url, payload):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector=self.connector) as session:
                response = await session.post(
                    url=url,
                    json=payload,
                )
                response_json = await response.json()
                return response_json
        except Exception as e:
            logger.error(e)
