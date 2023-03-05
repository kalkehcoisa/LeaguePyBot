import pytest


def test_player_init(get_player):
    from LPBv2 import (common, game)
    assert get_player
    assert isinstance(get_player.info, common.PlayerInfo)
    assert isinstance(get_player.stats, common.PlayerStats)
    assert isinstance(get_player.score, common.PlayerScore)
    assert isinstance(get_player.inventory, list)
    assert isinstance(get_player.location, str)
    assert isinstance(get_player, game.Player)


@pytest.mark.asyncio
async def test_player_update_info(get_player, update_data):
    from LPBv2.common import (
        PlayerInfo,
    )
    await get_player.update_info(update_data)
    assert get_player.info.name == "Supername"
    assert get_player.info.level == 1
    assert isinstance(get_player.info, PlayerInfo)


@pytest.mark.asyncio
async def test_player_update_stats(get_player, update_data):
    from LPBv2.common import (
        PlayerStats,
    )
    await get_player.update_stats(update_data)
    assert get_player.stats.maxHealth == 601.0
    assert isinstance(get_player.stats, PlayerStats)


@pytest.mark.asyncio
async def test_player_update_score(get_player, update_data):
    from LPBv2.common import (
        PlayerScore,
    )
    await get_player.update_score(update_data)
    assert get_player.score.creepScore == 100
    assert isinstance(get_player.score, PlayerScore)


@pytest.mark.asyncio
async def test_player_update_inventory(get_player, update_data):
    from LPBv2.common import (
        InventoryItem,
    )
    await get_player.update_inventory(update_data)
    assert isinstance(get_player.inventory, list)
    assert len(get_player.inventory) > 0
    assert isinstance(get_player.inventory[0], InventoryItem)
    assert get_player.inventory[0].itemID == 3854


@pytest.mark.asyncio
async def test_player_update_location(get_player, test_member, test_zone):
    from LPBv2.common import (
        PlayerInfo,
        MinimapZone,
    )
    await get_player.update_location(test_member)
    assert get_player.info.x == 100
    assert get_player.info.y == 100
    assert get_player.info.zone == test_zone
    assert isinstance(get_player.info.zone, MinimapZone)
    assert isinstance(get_player.info, PlayerInfo)


@pytest.mark.asyncio
async def test_player_update(get_player, update_data):
    from LPBv2.common import (
        InventoryItem,
        PlayerInfo,
        PlayerScore,
        PlayerStats,
    )
    await get_player.update(update_data)

    assert get_player.info.name == "Supername"
    assert get_player.info.level == 1
    assert isinstance(get_player.info, PlayerInfo)

    assert get_player.stats.maxHealth == 601.0
    assert isinstance(get_player.stats, PlayerStats)

    assert get_player.score.creepScore == 100
    assert isinstance(get_player.score, PlayerScore)

    assert isinstance(get_player.inventory, list)
    assert len(get_player.inventory) > 0
    assert isinstance(get_player.inventory[0], InventoryItem)
    assert get_player.inventory[0].itemID == 3854
