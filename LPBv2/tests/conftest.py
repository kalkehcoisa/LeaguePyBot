import os
import sys

import pytest

# Add the application folder to the Python path
app_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, app_folder)



@pytest.fixture
def get_connector():
    from LPBv2.game import GameConnector
    return GameConnector()

