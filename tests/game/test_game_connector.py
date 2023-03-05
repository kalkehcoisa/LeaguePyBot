


def test_game_connector_init(connector):
    from game import GameConnector
    assert connector
    assert connector.base_url
    assert connector.headers
    assert hasattr(connector, "request")
    assert isinstance(connector, GameConnector)


# only run if not in a game
# @pytest.mark.asyncio
# async def test_game_connector_request_not_connected(connector):
#     with pytest.raises(aiohttp.client_exceptions.ClientConnectorError):
#         assert await connector.request("/liveclientdata/allgamedata")
