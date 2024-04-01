from typing import Union
from BaseClasses import MultiWorld, CollectionState


class sotn_logic:
    player: int
    decimal_code: int # to be translated to hex for RAM addresses

    def __init__(self, world: MultiWorld, player: int, decimal_code: int):
        self.player = player


    def can_fly(self, state: CollectionState):
        return state.has('Soul of Bat', self.player) \
            or state.has_all({'Leap Stone', 'Gravity Boots'}, self.player) \
            or state.has_all({'Form of Mist', 'Power of Mist'}, self.player)

    def can_double_jump(self, state: CollectionState):
        return state.has('Leap Stone', self.player)

    def can_echo(self, state: CollectionState):
        return state.has_all({'Soul of Bat', 'Echo of Bat'}, self.player)

    def has_jewel(self, state: CollectionState):
        return state.has('Jewel of Open', self.player)

    def can_break_spikes(self, state: CollectionState):
        return state.has('Spike Breaker', self.player)

    def can_see_shaft(self, state: CollectionState):
        return state.has('Holy Glasses', self.player)

    def can_save_richter(self, state: CollectionState):
        return self.can_fly(state) and self.can_see_shaft(state)

    def has_both_rings(self, state: CollectionState):
        return state.has_all({'Gold Ring', 'Silver Ring'}, self.player)

    def can_stomp(self, state: CollectionState):
        """not vanilla logic, but easy to implement"""
        return state.has('Soul of Wolf', self.player)