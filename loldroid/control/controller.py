import asyncio

from .devices import KeyboardListener
from .devices import Keyboard, Mouse
from common import (
    average_position,
    riskiest_position,
    safest_position,
    make_minimap_coords,
    ZONES,
    find_closest_zone,
)
from logger import get_logger, debug_coro


logger = get_logger("loldroid.Controller")
shop_logger = get_logger("loldroid.Shop")

class Action:
    def __init__(
        self,
        *args,
        **kwargs
    ):
        self.mouse = Mouse()
        self.keyboard =Keyboard(sleep=0.1)
        self.hotkeys = kwargs.get("hotkeys")
        self.game = kwargs.get("game")

    @debug_coro(logger)
    async def attack_move(self, x: int, y: int):
        self.keyboard.input_key(self.hotkeys.attack_move)
        self.mouse.set_position_and_left_click(x, y)

    @debug_coro(logger)
    async def get_riskiest_ally_position(self):
        minions = self.game.game_units.units.ally_minions
        if minions:
            return riskiest_position(minions)

    @debug_coro(logger)
    async def skip_screen(self):
        self.keyboard.space()


class Combat(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset_x = 50
        self.offset_y = 50

    @debug_coro(logger)
    async def cast_spell(self, key, x: int, y: int):
        self.mouse.set_position(x + self.offset_x, y + self.offset_y)
        self.keyboard.input_key(key)

    @debug_coro(logger)
    async def level_up_abilities(self):
        if self.game.player.info.level in [1, 4, 5, 7, 9]:
            self.keyboard.input_key("Ctrl" + self.hotkeys.first_ability)
        elif self.game.player.info.level in [2, 14, 15, 17, 18]:
            self.keyboard.input_key("Ctrl" + self.hotkeys.second_ability)
        elif self.game.player.info.level in [3, 8, 10, 12, 13]:
            self.keyboard.input_key("Ctrl" + self.hotkeys.third_ability)
        else:
            self.keyboard.input_key("Ctrl" + self.hotkeys.ultimate_ability)

    @debug_coro(logger)
    async def cast_spells(self, x: int, y: int, ultimate=False):
        if ultimate:
            await self.cast_spell(self.hotkeys.ultimate_ability, x, y)
        await self.cast_spell(self.hotkeys.first_ability, x, y)
        await self.cast_spell(self.hotkeys.second_ability, x, y)
        await self.cast_spell(self.hotkeys.third_ability, x, y)

    @debug_coro(logger)
    async def attack(self, x: int, y: int):
        await self.attack_move(x + self.offset_x, y + self.offset_y)

    @debug_coro(logger)
    async def get_closest_enemy_position(self):
        minions = self.game.game_units.units.enemy_minions
        if minions:
            return safest_position(minions)

    @debug_coro(logger)
    async def get_average_enemy_position(self):
        minions = self.game.game_units.units.enemy_minions
        if minions:
            return average_position(minions)

    @debug_coro(logger)
    async def attack_minions(self):
        await self.game.game_flow.update_current_action("Attacking minions")
        pos = await self.get_closest_enemy_position()
        if pos:
            await self.attack(*pos)
        pos = await self.get_average_enemy_position()
        if await self.game.player.has_more_than_50_percent_mana() and pos:
            await asyncio.sleep(1)
            await self.cast_spells(*pos)

    @debug_coro(logger)
    async def get_closest_enemy_champion_position(self):
        champions = self.game.game_units.units.enemy_champions
        if champions:
            return safest_position(champions)

    @debug_coro(logger)
    async def attack_champion(self):
        await self.game.game_flow.update_current_action("Attacking champion")
        pos = await self.get_closest_enemy_champion_position()
        if pos:
            await self.attack(*pos)
            if await self.game.player.has_more_than_25_percent_mana() and pos:
                await self.cast_spells(*pos, ultimate=True)

    @debug_coro(logger)
    async def get_closest_enemy_building_position(self):
        buildings = self.game.game_units.units.enemy_buildings
        if buildings:
            return safest_position(buildings)

    @debug_coro(logger)
    async def attack_building(self):
        await self.game.game_flow.update_current_action("Attacking building")
        pos = await self.get_closest_enemy_building_position()
        pos_ally = await self.get_riskiest_ally_position()
        if pos and pos_ally:
            distance = ((pos[0] + self.offset_x) - (pos[1] + self.offset_y * 2)) - (
                pos_ally[0] - pos_ally[1]
            )
            if distance < 500:
                await self.attack(*pos)


class Movement(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro(logger)
    async def click_minimap(self, x: int, y: int):
        x, y = make_minimap_coords(x, y)
        self.mouse.set_position_and_right_click(x, y)

    @debug_coro(logger)
    async def recall(self):
        await self.game.game_flow.update_current_action("Recalling")
        self.keyboard.input_key(self.hotkeys.recall)

    @debug_coro(logger)
    async def go_to_lane(self):
        for zone in ZONES:
            if zone.name == "Top T1" and zone.team == self.game.player.info.team:
                await self.click_minimap(zone.x, zone.y)
                await self.game.game_flow.update_current_action(
                    f"Going to lane {zone.name}"
                )

    @debug_coro(logger)
    async def find_closest_ally_zone(self):
        x = 0
        y = 210
        if self.game.player.info.zone:
            x = self.game.player.info.zone.x
            y = self.game.player.info.zone.y
        safe_zones = [zone for zone in ZONES if zone.team == self.game.player.info.team]
        closest = find_closest_zone(x, y, zones=safe_zones)
        return closest

    @debug_coro(logger)
    async def fall_back(self, reason: str = None):
        zone = await self.find_closest_ally_zone()
        await self.game.game_flow.update_current_action(
            f"Falling back to {zone.name}. (reason: {reason})"
        )
        await self.click_minimap(zone.x, zone.y)

    @debug_coro(logger)
    async def follow_allies(self):
        await self.game.game_flow.update_current_action("Following allies")
        pos = await self.get_riskiest_ally_position()
        if pos:
            await self.attack_move(*pos)

    @debug_coro(logger)
    async def get_safest_ally_position(self):
        minions = self.game.game_units.units.ally_minions
        if minions:
            return safest_position(minions)

    @debug_coro(logger)
    async def lock_camera(self):
        self.keyboard.input_key(self.hotkeys.camera_lock)


class Shop(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build = kwargs.get('build')
        self.items: dict() = None
        self.version_items: str() = None

    @debug_coro(shop_logger)
    async def toggle_shop(self):
        self.keyboard.input_key(self.hotkeys.shop)

    @debug_coro(shop_logger)
    async def search_item(self):
        self.keyboard.input_key(self.hotkeys.search_shop)

    @debug_coro(shop_logger)
    async def buy_item(self, item_name: str):
        await self.search_item()
        shop_logger.debug(item_name)
        self.keyboard.input_word(item_name)
        self.keyboard.enter()

    @debug_coro(shop_logger)
    async def recursive_price_adjust(self, price, player_items, item):

        if item in player_items:
            return price - self.build.all_items.get(item).get('gold').get('total')

        composite = self.build.all_items.get(item).get('from')
        if composite:
            for component in composite:
                price = await self.recursive_price_adjust(
                    price, player_items, component
                )

        return price

    @debug_coro(logger)
    async def recursive_buy(self, shop_list):
        player_items = [str(item.itemID) for item in self.game.player.inventory]
        composite = self.build.all_items.get(shop_list[0]).get('from')
        price = self.build.all_items.get(shop_list[0]).get('gold').get('total')
        name = self.build.all_items.get(shop_list[0]).get('name')

        price = await self.recursive_price_adjust(price, player_items, shop_list[0])

        if (
            not shop_list[0] in player_items
            and self.game.player.info.currentGold >= price
            and len(player_items) < 7
        ):
            await self.buy_item(name)

        elif (
            not shop_list[0] in player_items
            and (self.game.player.info.currentGold < price or len(player_items) >= 7)
            and composite
        ):
            await self.recursive_buy(composite)

        if len(shop_list) <= 1 or (
            (self.game.player.info.currentGold < price or len(player_items) >= 7)
            and not composite
        ):
            return

        await self.recursive_buy(shop_list[1:])

    @debug_coro(logger)
    async def buy_build(self, build):
        await self.game.game_flow.update_current_action('Buying from shop')
        await self.toggle_shop()
        await asyncio.sleep(1)
        await self.recursive_buy(build)
        await asyncio.sleep(1)
        await self.toggle_shop()


class Usable(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro(logger)
    async def use_item(self, slot: int):
        slots = [
            self.hotkeys.item_slot_1,
            self.hotkeys.item_slot_2,
            self.hotkeys.item_slot_3,
            self.hotkeys.item_slot_4,
            self.hotkeys.item_slot_5,
            self.hotkeys.item_slot_6,
        ]
        self.keyboard.input_key(slots[slot])

    @debug_coro(logger)
    async def use_summoner_spell_1(self):
        self.keyboard.input_key(self.hotkeys.spell_1)

    @debug_coro(logger)
    async def use_summoner_spell_2(self):
        self.keyboard.input_key(self.hotkeys.spell_2)

    @debug_coro(logger)
    async def heal(self):
        slot = await self.game.player.get_consumable_slot()
        if isinstance(slot, int):
            await self.use_item(slot)
        await self.use_summoner_spell_2()


class Controller:
    def __init__(self, *args, **kwargs):
        self.action = Action(*args, **kwargs)
        self.combat = Combat(*args, **kwargs)
        self.movement = Movement(*args, **kwargs)
        self.usable = Usable(*args, **kwargs)
        self.shop = Shop(*args, **kwargs)
        self.listener = KeyboardListener()
