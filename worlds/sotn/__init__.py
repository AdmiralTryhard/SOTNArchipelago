import settings
import typing

from typing import Dict
from BaseClasses import Item, Location, MultiWorld, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld


class SOTNSettings(settings.Group):
    display_msgs: bool = True


class SOTNWorld(World):

    game = "Symphony of the Night"
    topology_present = False
    data_version = 0.1

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []
