from typing import List, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, CollectionState
from .Logic import SotnLogic


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None



def get_location_datas(world: Optional[MultiWorld], player: Optional[int]) -> List[LocationData]:
    
    
    logic = SotnLogic(world, player)
    # 135000 will be regular castle
    # 140000 will be inverted castle
    locations: List[LocationData] = [
        #62 locations to check
        LocationData('Prologue', 'Die monster You don\' belong in this world', 135000),
        LocationData('Prologue', 'Killed past Dracula', 135001),
        LocationData('Castle Entrance', 'Lost equipment', 135002),
        LocationData('Castle Entrance', 'Cube of Zoe', 135003),
        LocationData('Castle Entrance', 'Power of Wolf', 135032),
        LocationData('Alchemy Laboratory', 'Slogra', 135004),
        LocationData('Alchemy Laboratory', 'Gaibon', 135005),
        LocationData('Alchemy Laboratory', 'Maria talk', 135013, logic.has_jewel),
        LocationData('Alchemy Laboratory', 'Bat Card', 135006, logic.can_fly),
        LocationData('Marble Gallery', 'Meet Maria', 135007),
        LocationData('Marble Gallery', 'Spirit Orb', 135008),
        LocationData('Marble Gallery', 'Gravity Boots', 135009, logic.can_fly),
        LocationData('Outer Wall', 'Doppleganger10', 135010),
        LocationData('Outer Wall', 'Soul of Wolf', 135014),
        LocationData('Long Library', 'Talk to Shopkeeper', 135011),
        LocationData('Long Library', 'Shop Item', 135012),
        LocationData('Long Library', 'Faerie Scroll', 135013),
        LocationData('Long Library', 'Faerie Card', 135014, logic.has_some_upward_mobility),
        LocationData('Long Library', 'Lesser Demon', 135015, logic.has_some_upward_mobility),
        LocationData('Long Library', 'Soul of Bat', 135016, lambda state: logic.has_some_upward_mobility(state) and logic.can_mist(state)),
        LocationData('Clock Tower', 'Karasuman', 135017, logic.can_double_jump),
        LocationData('Royal Chapel', 'Hippogryph', 135018, lambda state: logic.has_jewel(state) or logic.can_double_jump(state)),
        LocationData('Royal Chapel', 'Post Boss Maria', 135019, lambda state: logic.has_jewel(state) or logic.can_double_jump(state)),
        LocationData('Royal Chapel', 'Maria behind doors', 135027, lambda state: logic.has_jewel(state) and logic.can_mist(state) and logic.can_break_spikes(state)),
        LocationData('Royal Chapel', 'Silver Ring', 135028, lambda state: logic.has_jewel(state) and logic.can_mist(state) and logic.can_break_spikes(state)),
        LocationData('Castle Keep', 'Leap Stone', 135020, lambda state: logic.has_jewel(state) or logic.can_double_jump(state)),
        LocationData('Castle Keep', 'Power of Mist', 135021, logic.can_fly),
        LocationData('Castle Keep', 'Richter', 135022, logic.can_save_richter),
        LocationData('Underground Caverns', 'Scylla Worm', 135023, logic.has_jewel),
        LocationData('Underground Caverns', 'Scylla', 135024, logic.has_jewel),
        LocationData('Underground Caverns', 'Merman Statue', 135025, logic.has_jewel),
        LocationData('Underground Caverns', 'Holy Symbol', 135026, lambda state: logic.has_jewel(state) and logic.can_safely_swim(state)),
        LocationData('Underground Caverns', 'Gold Ring', 135034, lambda state: logic.has_jewel(state) and logic.can_fly(state)),
        LocationData('Abandoned Mine', 'Cerberos', 135027, logic.access_catacombs),
        LocationData('Catacombs', 'Granfaloon', 135028, logic.access_catacombs),
        LocationData('Catacombs', 'Spike Breaker', 135029, lambda state: logic.access_catacombs(state) and (logic.can_echo(state) or logic.can_break_spikes(state))),
        LocationData('Olrox\'s Quarters', 'Olrox', 135030, logic.can_fly),
        LocationData('Olrox\'s Quarters', 'Echo of Bat', 135030, logic.can_fly),
        LocationData('Olrox\'s Quarters', 'Sword Card', 135031, logic.can_fly),
        LocationData('Colosseum', 'Form of Mist', 135033, logic.can_double_jump),
        LocationData('Colosseum', 'Minotaur', 135034, logic.can_double_jump),
        LocationData('Colosseum', 'Werewolf', 135035, logic.can_double_jump),
        LocationData('Alechemy Laboratory', 'Skill of Wolf', 135036, logic.can_fly),
        LocationData('Clock Tower', 'Fire of Bat', 135037, logic.can_fly),
        LocationData('Reverse Outer Wall', 'The Creaturue', 140000, logic.can_save_richter),
        LocationData('Reverse Outer Wall', 'Tooth of Vlad', 140001, logic.can_save_richter),
        LocationData('Anti Chapel', 'Heart of Vlad', 140002, logic.can_save_richter),
        LocationData('Anti Chapel', 'Medusa', 140003, logic.can_save_richter),
        LocationData('Necromancy Laboratory', 'Beelzebub', 140004, logic.can_save_richter),
        LocationData('Reverse Clock Tower', 'Darkwing Bat', 140005, logic.can_save_richter),
        LocationData('Reverse Colosseum', 'Trevor', 140006, logic.can_save_richter),
        LocationData('Reverse Clock Tower', 'Ring of Vlad', 140007, logic.can_save_richter),
        LocationData('Reverse Caverns', 'Doppleganger40', 140008, logic.can_save_richter),
        LocationData('Reverse Caverns', 'Force of Echo', 140013, logic.can_save_richter),
        LocationData('Cave', 'Death', 140009, logic.can_save_richter),
        LocationData('Cave', 'Eye of Vlad', 140010, logic.can_save_richter),
        LocationData('Floating Catacombs', 'Galamoth', 140011, logic.can_save_richter),
        LocationData('Floating Catacombs', 'Gas Cloud', 140012, logic.can_save_richter),
        LocationData('Black Marble Gallery', 'Shaft', 140013, lambda state: logic.can_save_richter(state) and logic.all_vlad(state)),
        LocationData('Death Wing\'s Lair', 'Akmodan', 140014, logic.can_save_richter),
        LocationData('Death Wing\'s Lair', 'Rib of Vlad', 140015, logic.can_save_richter),
        LocationData('Black Marble Gallery', 'Patricide', 140100, lambda state: logic.can_save_richter(state) and logic.all_vlad(state))
        #Think the location is 0x097420 combined with 0x3bf8e (fighting shaft/drac)
    ]

    return locations
