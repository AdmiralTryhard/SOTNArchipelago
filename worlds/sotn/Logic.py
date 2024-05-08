from typing import Union
from BaseClasses import MultiWorld, CollectionState


class SotnLogic:
    """all of these logical items are based on what the vanilla game expects you to be able to do as of right now
    possible extensions to this logic could be added like using wolf to be able to stomp and gain access to Olrox's
    Quarters early. Feel free to add that logic and options that could utilize it"""
    player: int

    def __init__(self, world: MultiWorld, player: int):
        self.player = player

    def can_fly(self, state: CollectionState):
        return state.has('Soul of Bat', self.player) \
            or state.has_all({'Leap Stone', 'Gravity Boots'}, self.player) \
            or state.has_all({'Form of Mist', 'Power of Mist'}, self.player)

    def can_double_jump(self, state: CollectionState):
        return state.has('Leap Stone', self.player) or self.can_fly(state)

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

    def can_safely_swim(self, state: CollectionState):
        return state.has_any({'Holy Symbol', 'Merman Statue'}, self.player)

    def can_high_jump(self, state: CollectionState):
        """just gravity boots isn't flight"""
        return state.has('Gravity Boots', self.player)

    def has_some_upward_mobility(self, state: CollectionState):
        return self.can_high_jump(state) or self.can_double_jump(state)

    def can_mist(self, state: CollectionState):
        return state.has('Form of Mist', self.player)

    def access_catacombs(self, state: CollectionState):
        return self.can_double_jump(state) and self.has_jewel(state)

    def all_vlad(self, state: CollectionState):
        return state.has_all({'Heart of Vlad', 'Tooth of Vlad', 'Rib of Vlad', 'Ring of Vlad', 'Eye of Vlad'}, self.player)

