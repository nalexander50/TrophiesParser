from typing import cast

import re

import patterns
from trophy_metal import TrophyMetal
from trophy_metadata_category import TrophyMetadataCategory

Trophy = dict[TrophyMetadataCategory, str | TrophyMetal]
TrophyList = list[Trophy]


def line_is_date(line: str):
    return re.search(patterns.DATE_PATTERN, line) is not None


def line_is_time(line: str):
    return re.search(patterns.TIME_PATTERN, line) is not None


def line_is_progress(line: str):
    return re.search(patterns.PRGORESS_PATTERN, line) is not None


def process(input_lines: list[str]) -> TrophyList:
    all_trophies: TrophyList = []

    current_trophy: Trophy = {}
    current_trophy_index = 0

    for line in input_lines:
        category = TrophyMetadataCategory(current_trophy_index)

        if category == TrophyMetadataCategory.UNLOCK_DATE and not line_is_date(line):
            current_trophy_index += 1
            category = TrophyMetadataCategory(current_trophy_index)

        if category == TrophyMetadataCategory.UNLOCK_TIME and not line_is_time(line):
            current_trophy_index += 1
            category = TrophyMetadataCategory(current_trophy_index)

        if category == TrophyMetadataCategory.PROGRESS and not line_is_progress(line):
            current_trophy_index += 1
            category = TrophyMetadataCategory(current_trophy_index)

        if category == TrophyMetadataCategory.METAL:
            current_trophy[category] = TrophyMetal.from_str(line.strip().replace(',', ''))
            all_trophies.append(current_trophy)
            current_trophy = {}
            current_trophy_index = 0
        else:
            current_trophy[category] = line.strip().replace(',', '')
            current_trophy_index += 1

    orderer_trophies = sorted(all_trophies,
                              reverse=True,
                              key=lambda data: cast(TrophyMetal, data[TrophyMetadataCategory.METAL]))

    return orderer_trophies
