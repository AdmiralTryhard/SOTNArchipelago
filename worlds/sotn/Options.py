from typing import Dict, Union, List
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict, OptionList



class MaxHealth(Range):
    """sets Alucard's maximum health value"""
    display_name = "Max Health"
    range_start = 1
    range_end = 9999
    default = 1000


sotn_options: Dict[str, Option] = {
    "Max Health": MaxHealth,
}