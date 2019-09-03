from enum import Enum, unique


@unique
class ETrophyMetal(Enum):
    Bronze = 'Bronze'
    Silver = 'Silver'
    Gold = 'Gold'
    Platinum = 'Platinum'


def allMetals():
    return [metal.name for metal in ETrophyMetal]
