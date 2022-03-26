from enum import IntEnum, unique


@unique
class ETrophyMetadataCategory(IntEnum):
    NAME = 0
    CRITERIA = 1
    UNLOCK_DATE = 2
    UNLOCK_TIME = 3
    PROGRESS = 4
    RARITY_PERCENT = 5
    RARITY_FLAVOR = 6
    METAL = 7


def allMetdataCategories():
    return [category.name for category in ETrophyMetadataCategory]
