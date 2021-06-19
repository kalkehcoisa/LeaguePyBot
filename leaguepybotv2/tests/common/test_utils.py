from leaguepybotv2.common.utils import *
from leaguepybotv2.common import CHAMPIONS
from leaguepybotv2.common.models import Match


def test_cast_to_bool_true():
    assert cast_to_bool("true") == True


def test_cast_to_bool_false():
    assert cast_to_bool("false") == False


def test_get_key_from_value():
    assert get_key_from_value(CHAMPIONS, 114) == "fiora"


def test_get_key_from_value_not_existing():
    assert get_key_from_value(CHAMPIONS, 999) == "Not found"


def test_atob():
    assert atob("Hello") == "SGVsbG8="


def test_pythagorean_distance_1():
    x = (0, 0)
    y = (0, 200)
    assert pythagorean_distance(x, y) == 200


def test_pythagorean_distance_1():
    x = (100, 200)
    y = (200, 200)
    assert pythagorean_distance(x, y) == 141.4213562373095


def test_pythagorean_distance_1():
    x = (0, 0)
    y = (200, 0)
    assert pythagorean_distance(x, y) == 200


def test_average_position():
    units = [Match(x=0, y=0), Match(x=100, y=0), Match(x=0, y=100), Match(x=100, y=100)]
    assert average_position(units) == (50, 50)
