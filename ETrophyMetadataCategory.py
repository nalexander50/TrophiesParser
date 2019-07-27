from enum import IntEnum, unique


@unique
class ETrophyMetadataCategory(IntEnum):
    NAME = 0
    CRITERIA = 1
    UNLOCK_DATE = 2
    UNLOCK_TIME = 3
    RARITY_PERCENT = 4
    RARITY_FLAVOR = 5
    METAL = 6


def allMetdataCategories():
    return [category.name for category in ETrophyMetadataCategory]
