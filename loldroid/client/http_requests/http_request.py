from ..connection.http_connection import HTTPConnection
from logger import debug_coro


class HTTPRequest:
    def __init__(self, client_data, *args, **kwargs):
        self.client_data = client_data
        self.http = HTTPConnection(client_data=client_data)

    async def request(self, **kwargs):
        response = await self.http.request(**kwargs)
        if response.status_code in [200, 201, 202, 203, 204, 205, 206]:
            return response
