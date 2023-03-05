from .http_request import HTTPRequest
from ...common import SummonerInfo
import asyncio
from ...logger import get_logger, debug_coro

logger = get_logger("LPBv2.Summoner")


class Summoner(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = None
        loop = asyncio.get_event_loop()
        loop.create_task(self.get_current_summoner())

    @debug_coro(logger)
    async def get_current_summoner(self):
        resp = await self.http.request(
            method="GET", endpoint="/lol-summoner/v1/current-summoner"
        )
        self.info = SummonerInfo(**resp.data)
