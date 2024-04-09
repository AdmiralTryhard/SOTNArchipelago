from typing import Dict, List, Set, Tuple, TextIO, Union, Any
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import sotn_items, link_item_names_to_category, filler_items
from .Locations import get_location_datas, EventId
from .Regions import create_regions_and_locations
from .Options import is_option_enabled, get_option_value, sotn_options
from worlds.AutoWorld import World, WebWorld




class SotnWebWorld(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "How to set up Castlevania: Symphony of the Night for multiworld fun",
        "English",
        "setup_en.md",
        "setup/en",
        ["Admiral Tryhard"]
    )



class SotnWorld(World):
    """Castlevania: Symphony of the Night is the initial game that defined the Metroidvania genre
    Make sure Dracula is defeated for real after finding out that Shaft has brought him back
    in this wonderful game filled with defining gameplay and voice acting"""
    option_definitions = sotn_options
    game = "sotn"
    topology_present = True
    data_version = 12
    web = SotnWebWorld()
    required_client_version = (0, 4, 4)

    item_name_to_id = {name: data.code for name, data in sotn_items.items()}
    location_name_to_id = {location.name: location.code for location in get_location_datas(None, None)}
    item_name_groups = link_item_names_to_category()

    def create_regions(self) -> None:
        """from .Regions"""
        create_regions_and_locations(self.multiworld, self.player)

    def create_items(self) -> None:
        self.create_and_assign_event_items()

        excluded_items: Set[str] = self.get_excluded_items()
        self.multiworld.itempool += self.get_item_pool(excluded_items)

    def set_rules(self) -> None:
        final_boss = "Black Marble Gallery: Patricide"
        self.multiworld.completion_condition[self.player] = lambda state: state.has(final_boss, self.player)

    def create_item(self, name: str) -> Item:
        data = sotn_items[name]

        if data.useful:
            classification = ItemClassification.useful
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        item = Item(name, classification, data.code, self.player)

        return item

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()

        for item in self.multiworld.precollected_items[self.player]:
            if item.name not in self.item_name_groups['Filler']:
                excluded_items.add(item.name)
        return excluded_items

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in sotn_items.items():
            if name not in excluded_items:
                for _ in range(data.count):
                    item = self.create_item(name)
                    pool.append(item)

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
            item = self.create_item(self.get_filler_item_name())
            pool.append(item)

        return pool

    def get_filler_item_name(self) -> str:
        # Life max up is only one for now, but there could very well be more like usables
        return self.multiworld.random.choice(filler_items)

    def create_and_assign_event_items(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            if location.address == EventId:
                item = Item(location.name, ItemClassification.progression, EventId, self.player)
                location.place_locked_item(item)
