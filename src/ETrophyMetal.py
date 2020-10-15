from enum import Enum, unique


@unique
class ETrophyMetal(Enum):

    Bronze = 0
    Silver = 1
    Gold = 2
    Platinum = 3

    @staticmethod
    def from_str(str_value: str):
        options = {
            'Bronze': ETrophyMetal.Bronze,
            'Silver': ETrophyMetal.Silver,
            'Gold': ETrophyMetal.Gold,
            'Platinum': ETrophyMetal.Platinum,
        }

        str_value = str_value.strip().title()

        if str_value in options:
            return options[str_value]
        else:
            return None

    def __str__(self):
        if self is ETrophyMetal.Bronze:
            return 'Bronze'
        elif self is ETrophyMetal.Silver:
            return 'Silver'
        elif self is ETrophyMetal.Gold:
            return 'Gold'
        elif self is ETrophyMetal.Platinum:
            return 'Platinum'
        return None

    def __lt__(self, other):
        if not isinstance(self, ETrophyMetal) or not isinstance(other, ETrophyMetal):
            return False
        return self.value < other.value

    def __eq__(self, other):
        if not isinstance(self, ETrophyMetal) or not isinstance(other, ETrophyMetal):
            return False
        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(self, ETrophyMetal) or not isinstance(other, ETrophyMetal):
            return False
        return self.value < other.value
        
