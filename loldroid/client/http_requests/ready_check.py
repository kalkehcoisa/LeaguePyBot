from .http_request import HTTPRequest

from logger import get_logger, debug_coro

logger = get_logger("loldroid.ReadyCheck")


class ReadyCheck(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro(logger)
    async def accept(self, event):
        searchState = event.data.get("searchState")
        playerResponse = event.data.get("readyCheck").get("playerResponse")
        state = event.data.get("readyCheck").get("state")
        if (
            (searchState == "Found" or state == "InProgress")
            and state not in ["EveryoneReady", "Error"]
            and playerResponse != "Accepted"
        ):
            response = await self.request(
                method="POST",
                endpoint="/lol-matchmaking/v1/ready-check/accept",
            )
            if response:
                logger.warning("Match found: Accepted ready check")
