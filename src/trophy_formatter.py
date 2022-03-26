from trophy_metal import TrophyMetal
from trophy_metadata_category import TrophyMetadataCategory

Trophy = dict[TrophyMetadataCategory, str | TrophyMetal]
TrophyList = list[Trophy]


def delimited(delimiter: str, trophy: Trophy, spaces: bool = False, delimiter_replacer: str = ' ', newline: bool = True) -> str:
    unlocked = TrophyMetadataCategory.UNLOCK_DATE in trophy and TrophyMetadataCategory.UNLOCK_TIME in trophy
    name = str(trophy[TrophyMetadataCategory.NAME])
    criteria = str(trophy[TrophyMetadataCategory.CRITERIA])
    metal = str(trophy[TrophyMetadataCategory.METAL])

    if delimiter_replacer is not None:
        for str_value in [name, criteria]:
            if delimiter in str_value:
                str_value.replace(delimiter, delimiter_replacer)

    char_space = ' '
    if spaces and not delimiter.endswith(char_space):
        delimiter = delimiter + char_space

    output = f'{unlocked}{delimiter}{False}{delimiter}{name}{delimiter}{criteria}{delimiter}{metal}'
    if newline:
        output = output + '\n'

    return output


def csv(trophy: Trophy, spaces: bool = False, delimiter_replacer: str = ' ', newline: bool = True) -> str:
    return delimited(',',
                     trophy,
                     spaces=spaces,
                     delimiter_replacer=delimiter_replacer,
                     newline=newline)


def piped(trophy: Trophy, spaces: bool = False, delimiter_replacer: str = ' ', newline: bool = True):
    return delimited('|',
                     trophy,
                     spaces=spaces,
                     delimiter_replacer=delimiter_replacer,
                     newline=newline)
