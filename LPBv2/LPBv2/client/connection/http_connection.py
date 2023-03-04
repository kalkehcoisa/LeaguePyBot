from threading import Lock

from aiohttp import ClientSession, BasicAuth

from .connection import Connection
from json import dumps
from ...common import ClientResponse, debug_coro
from ...logger import get_logger

logger = get_logger("LPBv2.HTTPConnection")


class HTTPConnection(Connection):
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
        super().__init__()

    @debug_coro
    async def request(self, **kwargs):
        async with ClientSession(
            auth=BasicAuth("riot", self.lockfile.auth_key),
            headers=self.headers,
        ) as session:
            endpoint = kwargs.pop("endpoint")
            params = {
                "method": kwargs.pop("method"),
                "url": self.make_url(endpoint),
            }
            if kwargs.get("payload"):
                params["data"] = dumps(kwargs.pop("payload"))
            try:
                response = await session.request(**params, ssl=False)
                data = await response.json()
                return ClientResponse(
                    endpoint=endpoint, data=data, status_code=response.status
                )
            except Exception as e:
                logger.error(e)

    def make_url(self, endpoint):
        return f"https://127.0.0.1:{self.lockfile.port}{endpoint}"
