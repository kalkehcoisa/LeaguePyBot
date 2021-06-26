from .. import *
from time import time


class LeaguePyBot:
    def __init__(self):
        self.client = Client()
        self.game = Game()
        self.minimap = Vision(
            bounding_box={
                "top": 1080 - 210,
                "left": 1920 - 210,
                "width": 210,
                "height": 210,
            }
        )
        self.screen = Vision()
        self.controller = Controller()
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.bot_loop())

    async def bot_loop(self):
        loop_time = time()
        while True:

            if await self.not_in_game():
                await self.reset()
                continue

            await self.computer_vision()
            await self.update_game_objects()
            await self.decide_actions()
            await self.execute_actions()

            self.FPS = round(float(1 / (time() - loop_time)), 2)
            loop_time = time()

        pass

    async def not_in_game(self):
        pass

    async def prepare_vision_objects(self):
        if not self.minimap.templates:
            names = await self.game.get_members()
            await self.minimap.load_templates(names=names, folder="champions_16x16")
        if not self.screen.templates:
            await self.screen.load_templates(
                names=["minion", "champion", "building_1", "building_2"],
                folder="units",
            )

    async def computer_vision(self):
        await self.prepare_vision_objects()
        await self.minimap.screenshot()
        await self.minimap.match(match_best_only=True)
        await self.screen.screenshot()
        await self.screen.match()

    async def update_member_location(self):
        for name in list(self.game.members):
            match = await self.minimap.get_match(name)
            if match:
                zone = await self.find_closest_zone(match.x, match.y)
                await self.game.update_member_location(name, match, zone)

    async def udpdate_units_position(self):
        await self.game.game_units.update(self.screen.matches)

    async def update_game_objects(self):
        await self.game.update_members(self.minimap.matches)
        await self.game.update_units(self.screen.matches)
        pass

    async def decide_actions(self):
        pass

    async def execute_actions(self):
        for action in self.actions:
            action.execute()

    # # misc
    #     - reset
    #     - update_FPS

    # # actions:
    #     - fall_back
    #     - heal
    #     - recall
    #     - cast_spells
    #     - attack
    #     - attack_building
    #     - attack_champion
    #     - attack_tower
    #     - follow_allies
    #     - move_minimap / go_to_lane
    #     - buy items

    # # calculations:
    #     - get_closest_enemy_building_position
    #     - get_closest_enemy_champion_position
    #     - get_closest_enemy_position
    #     - get_average_enemy_position
    #     - get_safest_ally_position
    #     - get_riskiest_ally_position
    #     - find_closest_ally_zone
    #     - find_closest_zone

    #     - get_units_position(units, function)
    #         - ally_minions
    #         - enemy_minions
    #         - enemy_champions
    #         - enemy_buildings
    #         - riskiest_position
    #         - safest_position
    #         - average_position

    # # computer vision:
    #     - locate_game_objects_AND_update
    #     - locate_champions_on_minimap_AND_update
