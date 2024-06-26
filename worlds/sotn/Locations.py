from typing import List, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, CollectionState
from .Logic import SotnLogic

EventId: Optional[int] = None

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None



def get_location_datas(world: Optional[MultiWorld], player: Optional[int]) -> List[LocationData]:
    """135000 will be regular castle
    140000 will be inverted castle
    it can be changed if this overlaps with other location checks that get added to Archipelago
    should you change location ID numbers, double check data/lua/connector_sotn.lua and update the value as well
    easy locations to start adding in would be the following:
    life vessel spots
    heart upgrades
    permanent equipment (alucard equipment for example)
    guarded items on pedestals like shield rod
    wall breakable items
    and so much more."""
    
    logic = SotnLogic(world, player)

    locations: List[LocationData] = [
        LocationData('Prologue', 'Die monster You don\'t belong in this world', 135000),
        LocationData('Prologue', 'Killed past Dracula', 135001),
        LocationData('Castle Entrance', 'Castle Entrance: Lost equipment', 135002),
        LocationData('Castle Entrance', 'Castle Entrance: Cube of Zoe', 135003),
        LocationData('Castle Entrance', 'Castle Entrance: Power of Wolf', 135032, logic.can_fly),
        LocationData('Alchemy Laboratory', 'Alchemy Laboratory: Slogra&Gaibon', 135004),
        LocationData('Alchemy Laboratory', 'Alchemy Laboratory: Maria asks about Richter', 135013, logic.has_jewel),
        LocationData('Alchemy Laboratory', 'Alchemy Laboratory: Bat Card', 135006, logic.can_fly),
        LocationData('Alchemy Laboratory', 'Alchemy Laboratory: Skill of Wolf', 135036, logic.can_fly),
        LocationData('Marble Gallery', 'Marble Gallery: Meet Maria', 135007),
        LocationData('Marble Gallery', 'Marble Gallery: Spirit Orb', 135008),
        LocationData('Marble Gallery', 'Marble Gallery: Gravity Boots', 135009, logic.can_fly),
        LocationData('Outer Wall', 'Outer Wall: Doppleganger10', 135010),
        LocationData('Outer Wall', 'Outer Wall: Soul of Wolf', 135014),
        LocationData('Long Library', 'Long Library: Talk to Shopkeeper', 135011),
        LocationData('Long Library', 'Long Library: Shop Item', 135038),
        LocationData('Long Library', 'Long Library: Faerie Scroll', 136013),
        LocationData('Long Library', 'Long Library: Faerie Card', 136014, logic.has_some_upward_mobility),
        LocationData('Long Library', 'Long Library: Lesser Demon', 135015, logic.has_some_upward_mobility),
        LocationData('Long Library', 'Long Library: Soul of Bat', 135016, lambda state: logic.has_some_upward_mobility(state) and logic.can_mist(state)),
        LocationData('Clock Tower', 'Clock Tower: Karasuman', 135017, logic.can_double_jump),
        LocationData('Royal Chapel', 'Royal Chapel: Hippogryph', 135018, lambda state: logic.has_jewel(state) or logic.can_double_jump(state)),
        LocationData('Royal Chapel', 'Royal Chapel: Post Boss Maria', 135019, lambda state: logic.has_jewel(state) or logic.can_double_jump(state)),
        LocationData('Royal Chapel', 'Royal Chapel: Maria behind doors', 135027, lambda state: logic.has_jewel(state) and logic.can_mist(state) and logic.can_break_spikes(state)),
        LocationData('Royal Chapel', 'Royal Chapel: Silver Ring', 135028, lambda state: logic.has_jewel(state) and logic.can_mist(state) and logic.can_break_spikes(state)),
        LocationData('Castle Keep', 'Castle Keep: Leap Stone', 135020, lambda state: logic.has_jewel(state) or logic.can_double_jump(state)),
        LocationData('Castle Keep', 'Castle Keep: Power of Mist', 135021, logic.can_fly),
        LocationData('Castle Keep', 'Castle Keep: Saved Richter', 135022, logic.can_save_richter),
        LocationData('Castle Keep', 'Castle Keep: Ghost Card', 136031, logic.can_fly),
        LocationData('Underground Caverns', 'Underground Caverns: Succubus', 135023, lambda state: logic.has_jewel(state) and logic.can_fly(state)),
        LocationData('Underground Caverns', 'Underground Caverns: Scylla', 135024, logic.has_jewel),
        LocationData('Underground Caverns', 'Underground Caverns: Merman Statue', 135025, logic.has_jewel),
        LocationData('Underground Caverns', 'Underground Caverns: Holy Symbol', 135026, lambda state: logic.has_jewel(state) and logic.can_safely_swim(state)),
        LocationData('Underground Caverns', 'Underground Caverns: Gold Ring', 135034, lambda state: logic.has_jewel(state) and logic.can_fly(state)),
        LocationData('Underground Caverns', 'Underground Caverns: PTSD Nightmare', 135040, lambda state: logic.has_jewel(state) and logic.can_fly(state)),
        LocationData('Abandoned Mine', 'Abandoned Mine: Cerberos', 136027, logic.access_catacombs),
        LocationData('Abandoned Mine', 'Abandonded Mine: Demon Card', 135012, logic.access_catacombs),
        LocationData('Catacombs', 'Catacombs: Granfaloon', 136028, logic.access_catacombs),
        LocationData('Catacombs', 'Catacombs: Spike Breaker', 135029, lambda state: logic.access_catacombs(state) and (logic.can_echo(state) or logic.can_break_spikes(state))),
        LocationData('Olrox\'s Quarters', 'Olrox\'s Quarters: Olrox', 135030, logic.can_fly),
        LocationData('Olrox\'s Quarters', 'Olrox\'s Quarters: Echo of Bat', 136030, logic.can_fly),
        LocationData('Olrox\'s Quarters', 'Olrox\'s Quarters: Sword Card', 135031, logic.can_fly),
        LocationData('Colosseum', 'Colosseum: Form of Mist', 135033, logic.can_double_jump),
        LocationData('Colosseum', 'Colosseum: See Evil Richter', 135039, logic.can_double_jump),
        LocationData('Colosseum', 'Colosseum: Minotaur', 136034, logic.can_double_jump),
        LocationData('Clock Tower', 'Clock Tower: Fire of Bat', 135037, logic.can_fly),
        LocationData('Reverse Outer Wall', 'Reverse Outer Wall: The Creature', 140000, logic.can_save_richter),
        LocationData('Reverse Outer Wall', 'Reverse Outer Wall: Tooth of Vlad', 140001, logic.can_save_richter),
        LocationData('Anti Chapel', 'Anti Chapel: Heart of Vlad', 140002, logic.can_save_richter),
        LocationData('Anti Chapel', 'Anti Chapel: Medusa', 140003, logic.can_save_richter),
        LocationData('Necromancy Laboratory', 'Necromancy Laboratory: Beelzebub', 140004, logic.can_save_richter),
        LocationData('Reverse Clock Tower', 'Reverse Clock Tower: Darkwing Bat', 140005, logic.can_save_richter),
        LocationData('Reverse Colosseum', 'Reverse Colosseum: Trevor', 140006, logic.can_save_richter),
        LocationData('Reverse Clock Tower', 'Reverse Clock Tower: Ring of Vlad', 140007, logic.can_save_richter),
        LocationData('Reverse Caverns', 'Reverse Caverns: Doppleganger40', 140008, logic.can_save_richter),
        LocationData('Reverse Caverns', 'Reverse Caverns: Force of Echo', 140013, logic.can_save_richter),
        LocationData('Cave', 'Cave: Confront Death', 140016, logic.can_save_richter),
        LocationData('Cave', 'Cave: Death', 140009, logic.can_save_richter),
        LocationData('Cave', 'Cave: Eye of Vlad', 140010, logic.can_save_richter),
        LocationData('Floating Catacombs', 'Floating Catacombs: Galamoth', 140011, logic.can_save_richter),
        LocationData('Floating Catacombs', 'Floating Catacombs: Gas Cloud', 140012, logic.can_save_richter),
        LocationData('Death Wing\'s Lair', 'Death Wing\'s Lair: Akmodan', 140014, logic.can_save_richter),
        LocationData('Death Wing\'s Lair', 'Death Wing\'s Lair: Rib of Vlad', 140015, logic.can_save_richter),

        LocationData('Black Marble Gallery', 'Black Marble Gallery: Patricide', EventId, lambda state: logic.can_save_richter(state) and logic.all_vlad(state))
    ]

    return locations
