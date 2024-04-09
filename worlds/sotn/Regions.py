from typing import List, Set, Dict, Optional, Callable
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, Location
from .Logic import SotnLogic
from .Locations import LocationData, get_location_datas



def create_regions_and_locations(world: MultiWorld, player: int):
    locations_per_region: Dict[str, List[LocationData]] = split_location_datas_per_region(
        get_location_datas(world, player))
    regions = [
        create_region(world, player, locations_per_region, 'Menu'),
        create_region(world, player, locations_per_region, 'Prologue'),
        create_region(world, player, locations_per_region, 'Castle Entrance'),
        create_region(world, player, locations_per_region, 'Alchemy Laboratory'),
        create_region(world, player, locations_per_region, 'Marble Gallery'),
        create_region(world, player, locations_per_region, 'Outer Wall'),
        create_region(world, player, locations_per_region, 'Long Library'),
        create_region(world, player, locations_per_region, 'Clock Tower'),
        create_region(world, player, locations_per_region, 'Royal Chapel'),
        create_region(world, player, locations_per_region, 'Castle Keep'),
        create_region(world, player, locations_per_region, 'Underground Caverns'),
        create_region(world, player, locations_per_region, 'Abandoned Mine'),
        create_region(world, player, locations_per_region, 'Catacombs'),
        create_region(world, player, locations_per_region, 'Olrox\'s Quarters'),
        create_region(world, player, locations_per_region, 'Colosseum'),
        create_region(world, player, locations_per_region, 'Reverse Keep'),
        create_region(world, player, locations_per_region, 'Forbidden Library'),
        create_region(world, player, locations_per_region, 'Reverse Outer Wall'),
        create_region(world, player, locations_per_region, 'Anti Chapel'),
        create_region(world, player, locations_per_region, 'Necromancy Laboratory'),
        create_region(world, player, locations_per_region, 'Reverse Clock Tower'),
        create_region(world, player, locations_per_region, 'Reverse Caverns'),
        create_region(world, player, locations_per_region, 'Cave'),
        create_region(world, player, locations_per_region, 'Floating Catacombs'),
        create_region(world, player, locations_per_region, 'Death Wing\'s Lair'),
        create_region(world, player, locations_per_region, 'Reverse Entrance'),
        create_region(world, player, locations_per_region, 'Reverse Colosseum'),
        create_region(world, player, locations_per_region, 'Black Marble Gallery')

    ]

    world.regions += regions

    logic = SotnLogic(world, player)

    connect_regions(world, player, 'Menu', 'Prologue'),
    connect_regions(world, player, 'Prologue', 'Castle Entrance'),
    connect_regions(world, player, 'Castle Entrance', 'Alchemy Laboratory'),
    connect_regions(world, player, 'Castle Entrance', 'Marble Gallery'),
    connect_regions(world, player, 'Alchemy Laboratory', 'Castle Entrance'),
    connect_regions(world, player, 'Alchemy Laboratory', 'Marble Gallery'),
    connect_regions(world, player, 'Alchemy Laboratory', 'Royal Chapel', logic.has_jewel),
    connect_regions(world, player, 'Marble Gallery', 'Castle Entrance'),
    connect_regions(world, player, 'Marble Gallery', 'Alchemy Laboratory'),
    connect_regions(world, player, 'Marble Gallery', 'Outer Wall'),
    connect_regions(world, player, 'Marble Gallery', 'Olrox\'s Quarters', logic.can_double_jump),
    connect_regions(world, player, 'Marble Gallery', 'Underground Caverns', logic.has_jewel),
    connect_regions(world, player, 'Outer Wall', 'Marble Gallery'),
    connect_regions(world, player, 'Outer Wall', 'Long Library'),
    connect_regions(world, player, 'Outer Wall', 'Clock Tower'),
    connect_regions(world, player, 'Long Library', 'Outer Wall'),
    connect_regions(world, player, 'Royal Chapel', 'Alchemy Laboratory', logic.has_jewel),
    connect_regions(world, player, 'Royal Chapel', 'Castle Keep'),
    connect_regions(world, player, 'Underground Caverns', 'Marble Gallery', logic.has_jewel),
    connect_regions(world, player, 'Underground Caverns', 'Abandoned Mine', logic.can_double_jump),
    connect_regions(world, player, 'Underground Caverns', 'Castle Entrance'),
    connect_regions(world, player, 'Abandoned Mine', 'Catacombs'),
    connect_regions(world, player, 'Catacombs', 'Abandoned Mine'),
    connect_regions(world, player, 'Clock Tower', 'Castle Keep', logic.can_double_jump),
    connect_regions(world, player, 'Olrox\'s Quarters', 'Colosseum'),
    connect_regions(world, player, 'Olrox\'s Quarters', 'Marble Gallery'),
    connect_regions(world, player, 'Olrox\'s Quarters', 'Royal Chapel'),
    connect_regions(world, player, 'Colosseum', 'Olrox\'s Quarters'),
    connect_regions(world, player, 'Colosseum', 'Royal Chapel'),
    connect_regions(world, player, 'Castle Keep', 'Royal Chapel'),
    connect_regions(world, player, 'Castle Keep', 'Clock Tower', logic.can_fly),
    connect_regions(world, player, 'Castle Keep', 'Reverse Keep', logic.can_save_richter),
    connect_regions(world, player, 'Reverse Keep', 'Castle Keep'),
    connect_regions(world, player, 'Reverse Keep', 'Reverse Clock Tower'),
    connect_regions(world, player, 'Reverse Keep', 'Anti Chapel'),
    connect_regions(world, player, 'Anti Chapel', 'Reverse Keep'),
    connect_regions(world, player, 'Anti Chapel', 'Necromancy Laboratory', logic.has_jewel),
    connect_regions(world, player, 'Anti Chapel', 'Death Wing\'s Lair'),
    connect_regions(world, player, 'Anti Chapel', 'Reverse Colosseum'),
    connect_regions(world, player, 'Death Wing\'s Lair', 'Reverse Colosseum'),
    connect_regions(world, player, 'Death Wing\'s Lair', 'Necromancy Laboratory'),
    connect_regions(world, player, 'Death Wing\'s Lair', 'Anti Chapel'),
    connect_regions(world, player, 'Necromancy Laboratory', 'Anti Chapel', logic.has_jewel),
    connect_regions(world, player, 'Necromancy Laboratory', 'Black Marble Gallery'),
    connect_regions(world, player, 'Necromancy Laboratory', 'Reverse Entrance'),
    connect_regions(world, player, 'Black Marble Gallery', 'Death Wing\'s Lair'),
    connect_regions(world, player, 'Black Marble Gallery', 'Reverse Outer Wall'),
    connect_regions(world, player, 'Black Marble Gallery', 'Necromancy Laboratory'),
    connect_regions(world, player, 'Black Marble Gallery', 'Reverse Entrance'),
    connect_regions(world, player, 'Black Marble Gallery', 'Reverse Caverns'),
    connect_regions(world, player, 'Reverse Outer Wall', 'Necromancy Laboratory'),
    connect_regions(world, player, 'Reverse Outer Wall', 'Forbidden Library'),
    connect_regions(world, player, 'Reverse Outer Wall', 'Reverse Clock Tower'),
    connect_regions(world, player, 'Reverse Clock Tower', 'Reverse Keep'),
    connect_regions(world, player, 'Reverse Clock Tower', 'Reverse Outer Wall'),
    connect_regions(world, player, 'Reverse Caverns', 'Black Marble Gallery'),
    connect_regions(world, player, 'Reverse Caverns', 'Reverse Entrance'),
    connect_regions(world, player, 'Reverse Caverns', 'Cave'),
    connect_regions(world, player, 'Cave', 'Reverse Caverns'),
    connect_regions(world, player, 'Cave', 'Floating Catacombs'),
    connect_regions(world, player, 'Floating Catacombs', 'Cave'),
    connect_regions(world, player, 'Reverse Colosseum', 'Anti Chapel'),
    connect_regions(world, player, 'Reverse Colosseum', 'Death Wing\'s Lair'),
    connect_regions(world, player, 'Reverse Entrance', 'Reverse Caverns'),
    connect_regions(world, player, 'Reverse Entrance', 'Necromancy Laboratory'),
    connect_regions(world, player, 'Reverse Entrance', 'Black Marble Gallery'),
    connect_regions(world, player, 'Forbidden Library', 'Reverse Outer Wall'),



def verify_all_locations_in_a_valid_region(regions: List[Region], region_names: Set[str]):
    existing_regions: Set[str] = set()

    for region in regions:
        existing_regions.add(region.name)

    if region_names - existing_regions:
        raise Exception("SOTN: the following regions are used in locations: {}, but no such region exists".format(region_names - existing_regions))



def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = Location(player, location_data.name, location_data.code, region)

    if location_data.rule:
        location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True
    return location



def split_location_datas_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)
    return per_region

def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)
    return region


def connect_regions(world: MultiWorld, player: int, source: str, destination: str,
                    rule: Optional[Callable[[CollectionState], bool]]=None):

    source_region = world.get_region(source, player)
    destination_region = world.get_region(destination, player)

    connection = Entrance(player, "", source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(destination_region)