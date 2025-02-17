from common import Units, Match
from typing import List

from logger import get_logger, debug_coro
logger = get_logger("loldroid.Game")

class GameUnits:
    def __init__(self):
        self.units = Units()

    @debug_coro(logger)
    async def update(self, matches: List[Match]):
        await self.clear_units()
        for match in matches:
            if match.team == "ORDER":
                if match.name == "minion":
                    self.units.ally_minions.append(match)
                    self.units.nb_ally_minions += 1
                if match.name == "champion":
                    self.units.ally_champions.append(match)
                    self.units.nb_ally_champions += 1
                if match.name == "building":
                    self.units.ally_buildings.append(match)
                    self.units.nb_ally_buildings += 1
            else:
                if match.name == "minion":
                    self.units.enemy_minions.append(match)
                    self.units.nb_enemy_minions += 1
                if match.name == "champion":
                    self.units.enemy_champions.append(match)
                    self.units.nb_enemy_champions += 1
                if match.name == "building":
                    self.units.enemy_buildings.append(match)
                    self.units.nb_enemy_buildings += 1

    @debug_coro(logger)
    async def clear_units(self):
        self.units = Units()

    @debug_coro(logger)
    async def is_minions_present(self):
        return self.units.nb_enemy_minions + self.units.nb_ally_minions > 0

    @debug_coro(logger)
    async def get_game_units(self):
        return self.units
