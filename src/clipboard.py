import sys
import re
import pyperclip

from ETrophyMetadataCategory import ETrophyMetadataCategory
from ETrophyMetal import ETrophyMetal


def looks_like_trophy_input(str_input):
    has_platinum = 'Platinum' in str_input
    has_gold = 'Gold' in str_input
    has_silver = 'Silver' in str_input
    has_bronze = 'Bronze' in str_input
    has_rarity = 'COMMON' in str_input or 'RARE' in str_input
    return has_bronze and has_silver and has_gold and has_platinum and has_rarity


def line_is_date(line):
    date_pattern = r'\d{1,2}(th|st|nd|rd)\s*.{3}\s*20\d{2}'
    return re.search(date_pattern, line) is not None


def line_is_time(line):
    time_pattern = r'\d{1,2}:\d{2}:\d{2}\s*(am|AM|pm|PM)'
    return re.search(time_pattern, line) is not None


def clipboard_copy_output(ordered_data):
    output_lines = []

    for data in ordered_data:
        unlocked = ETrophyMetadataCategory.UNLOCK_DATE in data and ETrophyMetadataCategory.UNLOCK_TIME in data
        name = data[ETrophyMetadataCategory.NAME]
        criteria = data[ETrophyMetadataCategory.CRITERIA]
        metal = str(data[ETrophyMetadataCategory.METAL])

        output_line = f'{unlocked},{False},{name},{criteria},{metal}'
        output_lines.append(output_line)

    output = '\n'.join(output_lines)
    pyperclip.copy(output)
    print(output)


def build_invalid_metal_message(invalid_value, current_lines):
    base_msg = 'Error: Invalid metal. Are you sure this was Trophy data?\n\n'
    invalid_msg = 'Invalid Metal Value: ' + invalid_value.strip().replace(',', '')
    lines_base_msg = 'Lines:'
    lines_details_msg = '\n'.join(['\t' + cl.strip() for cl in current_lines])
    lines_msg = lines_base_msg + '\n' + lines_details_msg
    return base_msg + invalid_msg + '\n\n' + lines_msg


def main():
    clipboard_input = str(pyperclip.paste())

    if clipboard_input is None or clipboard_input == '':
        exit('Error: Expected clipboard input. Clipboard is empty.')

    if not looks_like_trophy_input(clipboard_input):
        exit('Error: Clipbard input doesn\'t look like Trophy data.')

    input_lines = [
        line.strip().replace('\t', '')
        for line
        in clipboard_input.split('\n')
        if line is not None and line.strip() != ''
    ]

    if len(input_lines) < 2:
        exit('Error: Expected multiple lines of clipboard input')

    all_data = []

    current_data = dict()
    current_data_index = 0
    current_lines = []

    for line in input_lines:
        current_lines.append(line)
        category = ETrophyMetadataCategory(current_data_index)

        if category == ETrophyMetadataCategory.UNLOCK_DATE and not line_is_date(line):
            current_data_index += 1
            category = ETrophyMetadataCategory(current_data_index)

        if category == ETrophyMetadataCategory.UNLOCK_TIME and not line_is_time(line):
            current_data_index += 1
            category = ETrophyMetadataCategory(current_data_index)

        if category == ETrophyMetadataCategory.METAL:
            metal = ETrophyMetal.from_str(line.strip().replace(',', ''))

            if metal is None:
                msg = build_invalid_metal_message(line.strip().replace(',', ''), current_lines)
                exit(msg)

            current_data[category] = metal
            all_data.append(current_data)
            current_data = dict()
            current_data_index = 0
            current_lines = []
        else:
            current_data[category] = line.strip().replace(',', '')
            current_data_index += 1

    try:
        ordered_data = sorted(all_data, reverse=True, key=lambda data: data[ETrophyMetadataCategory.METAL])
    except:
        sys.exit('Error: Invalid data. Are you sure this was Trophy data?')

    clipboard_copy_output(ordered_data)


if __name__ == '__main__':
    main()
