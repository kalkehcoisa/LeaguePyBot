from LPBv2.common import WebSocketEventResponse
from .http_request import HTTPRequest
from ...logger import get_logger, debug_coro


logger = get_logger("LPBv2.Client")


class Notifications(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro(logger)
    async def get_endofgame_celebrations(self):
        response = await self.request(
            method="GET", endpoint="/lol-pre-end-of-game/v1/currentSequenceEvent"
        )
        celebration = response.data.get("name")
        return celebration

    @debug_coro(logger)
    async def skip_mission_celebrations(self):
        celebration = await self.get_endofgame_celebrations()
        await self.request(
            method="POST", endpoint=f"/lol-pre-end-of-game/v1/complete/{celebration}"
        )

    @debug_coro(logger)
    async def dismiss_notifications_at_eog(self, event: WebSocketEventResponse):
        if event.data in ["WaitingForStats", "PreEndOfGame"]:
            await self.skip_mission_celebrations()
