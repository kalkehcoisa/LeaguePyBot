import pytest
from LPBv2.common import GameEvent


@pytest.fixture
def game_flow():
    from LPBv2.game import GameFlow
    return GameFlow()


events_data = [
    {"EventID": 0, "EventName": "GameStart", "EventTime": 0.01637154631316662},
    {"EventID": 1, "EventName": "MinionsSpawning", "EventTime": 65.038818359375},
    {
        "Assisters": [],
        "EventID": 2,
        "EventName": "ChampionKill",
        "EventTime": 194.25624084472656,
        "KillerName": "KillerChamp",
        "VictimName": "VictimChamp",
    },
    {
        "EventID": 3,
        "EventName": "FirstBlood",
        "EventTime": 194.25624084472656,
        "Recipient": "KillerChamp",
    },
]

game_data = {
    "gameMode": "CLASSIC",
    "gameTime": 300.0,
    "mapName": "Map11",
    "mapNumber": 11,
    "mapTerrain": "Default",
}


def test_game_flow_init(game_flow):
    assert game_flow
    assert isinstance(game_flow.events, list)
    assert isinstance(game_flow.time, float)
    assert isinstance(game_flow.is_ingame, bool)
    assert isinstance(game_flow.current_action, str)
    assert isinstance(game_flow, GameFlow)
    assert hasattr(game_flow, "update")
    assert hasattr(game_flow, "update_is_ingame")
    assert hasattr(game_flow, "update_events")
    assert hasattr(game_flow, "update_current_action")


@pytest.mark.asyncio
async def test_update_is_ingame(game_flow):
    await game_flow.update_is_ingame(True)
    assert game_flow.is_ingame == True


@pytest.mark.asyncio
async def test_update_events(game_flow):
    await game_flow.update_events(events_data)
    assert len(game_flow.events) == 4
    assert isinstance(game_flow.events[0], GameEvent)


@pytest.mark.asyncio
async def test_update_time(game_flow):
    await game_flow.update_time(game_data)
    assert game_flow.time == 300.0


@pytest.mark.asyncio
async def test_game_flow_update(game_flow):
    await game_flow.update(events_data=events_data, game_data=game_data)
    assert len(game_flow.events) == 4
    assert isinstance(game_flow.events[0], GameEvent)
    assert game_flow.time == 300.0
