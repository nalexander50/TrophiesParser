from __future__ import annotations

from enum import Enum, unique


@unique
class TrophyMetal(Enum):

    BRONZE = 0
    SILVER = 1
    GOLD = 2
    PLATINUM = 3

    @staticmethod
    def from_str(str_value: str) -> TrophyMetal:
        options = {
            'Bronze': TrophyMetal.BRONZE,
            'Silver': TrophyMetal.SILVER,
            'Gold': TrophyMetal.GOLD,
            'Platinum': TrophyMetal.PLATINUM,
        }

        str_value = str_value.strip().title()

        if str_value in options:
            return options[str_value]
        else:
            raise ValueError(f'Invalid Metal ({str_value})')

    def __str__(self) -> str:
        if self is TrophyMetal.BRONZE:
            return 'Bronze'
        elif self is TrophyMetal.SILVER:
            return 'Silver'
        elif self is TrophyMetal.GOLD:
            return 'Gold'
        elif self is TrophyMetal.PLATINUM:
            return 'Platinum'
        return '<uknown>'

    def __lt__(self, other: object) -> bool:
        if not isinstance(self, TrophyMetal) or not isinstance(other, TrophyMetal):
            return False
        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(self, TrophyMetal) or not isinstance(other, TrophyMetal):
            return False
        return self.value == other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(self, TrophyMetal) or not isinstance(other, TrophyMetal):
            return False
        return self.value > other.value
