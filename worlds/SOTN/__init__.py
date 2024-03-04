import typing

from typing import Dict
from BaseClasses import Item, Location, MultiWorld, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld


class SOTNWorld(World):
    """
    Final Fantasy 1, originally released on the NES on 1987, is the game that started the beloved, long running series.
    The randomizer takes the original 8-bit Final Fantasy game for NES (USA edition) and allows you to
    shuffle important aspects like the location of key items, the difficulty of monsters and fiends,
    and even the location of towns and dungeons.
    Part puzzle and part speed-run, it breathes new life into one of the most influential games ever made.
    """

    settings: typing.ClassVar[SOTNSettings]
    settings_key = "SOTN_options"
    game = "Symphony of the Night"
    topology_present = False
    data_version = 0.1

    SOTN_items = SOTNItems()
    SOTN_locations = SOTNLocations()
    item_name_groups = SOTN_items.get_item_names_per_category()
    item_name_to_id = SOTN_items.get_item_name_to_code_dict()
    location_name_to_id = SOTN_locations.get_location_name_to_address_dict()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []


    def create_item(self, name: str) -> Item:
        return self.SOTN_items.generate_item(name, self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has(CHAOS_TERMINATED_EVENT, self.player)

    def create_items(self):
        items = get_options(self.multiworld, 'items', self.player)

        items = [self.create_item(name) for name, data in items.items() for x in range(data['count']) if name not in
                 self.locked_items]

        self.multiworld.itempool += items

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        return slot_data

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(["Heal", "Pure", "Soft", "Tent", "Cabin", "House"])


def get_options(world: MultiWorld, name: str, player: int):
    return getattr(world, name, None)[player].value
