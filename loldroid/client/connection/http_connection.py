from threading import Lock

from aiohttp import ClientSession, BasicAuth

from ..data import ClientData
from json import dumps
from common import ClientResponse
from logger import get_logger, debug_coro

logger = get_logger('loldroid.HTTPConnection')


class HTTPConnection:
    __instance = None
    _lock: Lock = Lock()

    headers: dict

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls.__instance is None:
                instance = super().__call__(*args, **kwargs)
                cls.__instance = instance
        return cls.__instance

    def __init__(self, client_data):
        self.client_data = client_data
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @debug_coro(logger)
    async def request(self, **kwargs):
        async with ClientSession(
            auth=BasicAuth('riot', self.client_data.auth_key),
            headers=self.headers,
        ) as session:
            endpoint = kwargs.pop('endpoint')
            params = {
                'method': kwargs.pop('method'),
                'url': self.make_url(endpoint),
            }
            if kwargs.get('payload'):
                params['data'] = dumps(kwargs.pop('payload'))
            try:
                response = await session.request(**params, ssl=False)
                data = await response.json()
                return ClientResponse(
                    endpoint=endpoint, data=data, status_code=response.status
                )
            except Exception as e:
                logger.error(e)

    def make_url(self, endpoint):
        return f'https://127.0.0.1:{self.cli_data.port}{endpoint}'
