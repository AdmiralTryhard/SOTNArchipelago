import json
from pathlib import Path
from typing import Dict, NamedTuple, List, Optional

from BaseClasses import Region, Location, MultiWorld


class LocationData(NamedTuple):
    name: str
    address: int


class SOTNLocations:
    _location_table: List[LocationData] = []
    _location_table_lookup: Dict[str, LocationData] = {}

    def _populate_item_table_from_data(self):
        base_path = Path(__file__).parent
        file_path = (base_path / "data/locations.json").resolve()
        with open(file_path) as file:
            locations = json.load(file)
            self._location_table = [LocationData(name, code) for name, code in locations.items()]
            self._location_table_lookup = {item.name: item for item in self._location_table}

    @staticmethod
    def create_menu_region(player: int, locations: Dict[str, int]
                           , world: MultiWorld) -> Region:
        menu_region = Region("Menu", player, world)
        for name, address in locations.items():
            location = Location(player, name, address, menu_region)
            menu_region.locations.append(location)
        return menu_region
