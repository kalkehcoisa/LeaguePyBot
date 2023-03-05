
import pytest


@pytest.mark.asyncio
async def test_websocket_empty_events(websocket):
    assert isinstance(websocket.events, list)
    assert len(websocket.events) == 0


@pytest.mark.asyncio
async def test_websocket_event_constructor():
    from common import WebSocketEvent
    websocket = WebSocket(
        events=[WebSocketEvent(endpoint="/", type="UPDATE", function=say_hello)]
    )
    assert isinstance(websocket.events, list)
    assert len(websocket.events) > 0
    assert isinstance(websocket.events[0], WebSocketEvent)


@pytest.mark.asyncio
async def test_websocket_register_event(websocket):
    from common import WebSocketEvent
    await websocket.register_event(
        WebSocketEvent(endpoint="/", type="UPDATE", function=say_hello)
    )
    assert isinstance(websocket.events, list)
    assert len(websocket.events) > 0
    assert isinstance(websocket.events[0], WebSocketEvent)


@pytest.mark.asyncio
async def test_websocket_match_websocket():
    from client import WebSocket
    from common import WebSocketEvent
    websocket = WebSocket(
        events=[
            WebSocketEvent(endpoint="/my_endpoint", type="UPDATE", function=say_hello)
        ]
    )
    data = {"uri": "/my_endpoint", "eventType": "UPDATE", "data": "Bob"}
    await websocket.match_websocket(data)


@pytest.mark.asyncio
async def say_hello(event):
    from common import WebSocketEventResponse
    assert isinstance(event, WebSocketEventResponse)
    print(f"Hello {event.data}")
