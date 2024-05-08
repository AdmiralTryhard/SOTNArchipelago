from typing import Dict, Union, List
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict, OptionList



class MaxHealth(Range):
    """sets Alucard's maximum health value. TODO: Lua implementation still needed"""
    display_name = "Max Health"
    range_start = 1
    range_end = 9999
    default = 1000


sotn_options: Dict[str, Option] = {
    "MaxHealth": MaxHealth
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
