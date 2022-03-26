from typing import Tuple

import sys
import re
import os

from trophy_metadata_category import TrophyMetadataCategory
from trophy_metal import TrophyMetal


def parse_args() -> Tuple[str, str]:
    input_path = os.path.join(os.getcwd(), 'input.txt')
    output_path = os.path.join(os.getcwd(), 'output.csv')

    if len(sys.argv) >= 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    return (input_path, output_path)


def line_is_date(line: str):
    date_pattern = r'\d{1,2}(th|st|nd|rd)\s*.{3}\s*20\d{2}'
    return re.search(date_pattern, line) is not None


def line_is_time(line: str):
    time_pattern = r'\d{1,2}:\d{2}:\d{2}\s*(am|AM|pm|PM)'
    return re.search(time_pattern, line) is not None


def line_is_progress(line: str):
    prgoress_pattern = r'\d+\/\d+'
    return re.search(prgoress_pattern, line) is not None


def build_output_line(data: dict[TrophyMetadataCategory, str | TrophyMetal]):
    unlocked = TrophyMetadataCategory.UNLOCK_DATE in data and TrophyMetadataCategory.UNLOCK_TIME in data
    name = data[TrophyMetadataCategory.NAME]
    criteria = data[TrophyMetadataCategory.CRITERIA]
    metal = str(data[TrophyMetadataCategory.METAL])

    output_line = f'{unlocked},{False},{name},{criteria},{metal}\n'
    return output_line


def main(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf8') as input_file:
        with open(output_path, 'w', encoding='utf8') as output_file:
            all_data: list[dict[TrophyMetadataCategory, str | TrophyMetal]] = []

            current_data = {}
            current_data_index = 0

            for line in input_file:
                category = TrophyMetadataCategory(current_data_index)

                if category == TrophyMetadataCategory.UNLOCK_DATE and not line_is_date(line):
                    current_data_index += 1
                    category = TrophyMetadataCategory(current_data_index)

                if category == TrophyMetadataCategory.UNLOCK_TIME and not line_is_time(line):
                    current_data_index += 1
                    category = TrophyMetadataCategory(current_data_index)

                if category == TrophyMetadataCategory.PROGRESS and not line_is_progress(line):
                    current_data_index += 1
                    category = TrophyMetadataCategory(current_data_index)

                if category == TrophyMetadataCategory.METAL:
                    current_data[category] = TrophyMetal.from_str(line.strip().replace(',', ''))
                    all_data.append(current_data)
                    current_data = {}
                    current_data_index = 0
                else:
                    current_data[category] = line.strip().replace(',', '')
                    current_data_index += 1

            ordered_data = sorted(all_data, reverse=True, key=lambda data: data[TrophyMetadataCategory.METAL])
            for data in ordered_data:
                output_file.write(build_output_line(data))


if __name__ == '__main__':
    arg_input_path, arg_output_path = parse_args()
    main(arg_input_path, arg_output_path)
