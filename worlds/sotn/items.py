from typing import Dict, Set, Tuple, NamedTuple


class ItemData(NamedTuple):
    category: str
    code: int
    count: int = 1
    progression: bool = False
    useful: bool = False


sotn_items: Dict[str, ItemData] = {

    "Soul of Bat": ItemData('Relic', 620900, progression=True),
    "Echo of Bat": ItemData('Relic', 620902, progression=True),
    "Soul of Wolf": ItemData('Relic', 620904, progression=True),
    "Skill of Wolf": ItemData('Relic', 620906, useful=True),
    "Power of Wolf": ItemData('Relic', 620905, progression=True),
    "Form of Mist": ItemData('Relic', 620907, progression=True),
    "Power of Mist": ItemData('Relic', 620908, progression=True),
    "Gravity Boots": ItemData('Relic', 620912, progression=True),
    "Leap Stone": ItemData('Relic', 620913, progression=True),
    "Jewel of Open": ItemData('Relic', 620916, progression=True),
    "Merman Statue": ItemData('Relic', 620917, progression=True),
    "Demon Card": ItemData('Relic', 620921, useful=True),
    "Heart of Vlad": ItemData('Relic', 620923, progression=True),
    "Tooth of Vlad": ItemData('Relic', 620924, progression=True),
    "Rib of Vlad": ItemData('Relic', 620925, progression=True),
    "Ring of Vlad": ItemData('Relic', 620926, progression=True),
    "Eye of Vlad": ItemData('Relic', 620927, progression=True),
    "Holy Glasses": ItemData('progressive equipment', 621141, progression=True),
    "Spike Breaker": ItemData('progressive equipment', 621121, progression=True),
    "Gold Ring": ItemData('progressive equipment', 621179, progression=True),
    "Silver Ring": ItemData('progressive equipment', 621180, progression=True),
    "Bat Card": ItemData('Relic', 620918),
    "Ghost Card": ItemData('Relic', 620919),
    "Faerie Card": ItemData('Relic', 620920, useful=True),
    "Sword Card": ItemData('Relic', 620922, useful=True),
    "Faerie Scroll": ItemData('Relic', 620915),
    "Cube of Zoe": ItemData('Relic', 620910, useful=True),
    "Spirit Orb": ItemData('Relic', 620911)
    "Fire of Bat": ItemData('Relic', 620901)
    "Force of Echo": ItemData('Relic', 620903)
    "Gas Cloud": ItemData('Relic', 620909, useful=True),
    "Holy Symbol": ItemData('Relic', 620914, progression=True)
}
