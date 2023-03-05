import os
import sys
from collections import defaultdict
from unittest.mock import patch, MagicMock, Mock

import pytest

# Add the application folder to the Python path
app_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, app_folder)


@pytest.fixture
def action():
    from control.controller import Action
    return Action()


@pytest.fixture
def champ_select():
    from client import ChampSelect
    from tests.mocks.mock_http_connection import MockHTTPConnection
    return ChampSelect(connection=MockHTTPConnection())


@pytest.fixture
def combat():
    from control.controller import Combat
    return Combat()


@pytest.fixture
def connector():
    from game import GameConnector
    return GameConnector()


@pytest.fixture
def http_connection():
    from client import HTTPConnection
    return HTTPConnection()


@pytest.fixture
def lockfile():
    from client import ClientData

    mock_process = Mock(**{'pid': 111111, 'name.return_value': 'LeagueClientUx.exe'})
    mock_cmd_args = {
        'app-pid': '111111',
        'app-port': '1234',
        'remoting-auth-token': 'aaaaahhhh token',
        'install-directory': '/path/install/nowhere'
    }
    lock = ClientData()
    with patch.object(lock, 'return_ux_process', return_value=iter([mock_process])):
        with patch.object(lock, 'parse_cmdline_args', return_value=mock_cmd_args):
            yield lock


@pytest.fixture
def websocket():
    from client import WebSocket
    return WebSocket()
