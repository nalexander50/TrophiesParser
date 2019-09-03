import sys
from os import getcwd
from os.path import join

from ETrophyMetadataCategory import ETrophyMetadataCategory
from ETrophyMetal import ETrophyMetal, allMetals


def parse_args():
    input_path = join(getcwd(), 'input.txt')
    output_path = join(getcwd(), 'output.csv')

    try:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    except:
        pass
    finally:
        return (input_path, output_path)


def main(input_file, output_file):
    output_file.write(header())

    is_name_next = True
    is_criteria_next = False
    is_unlock_date_next = False
    is_metal_next = False

    for line in input_file:
        category = None

        if is_name_next:
            category = ETrophyMetadataCategory.NAME
        elif is_criteria_next:
            category = ETrophyMetadataCategory.CRITERIA
        elif is_unlock_date_next and is_unlock_date_line(line):
            category = ETrophyMetadataCategory.UNLOCK_DATE
        elif is_unlock_date_next and is_metal_line(line):
            output_file.write(process_line(
                None, ETrophyMetadataCategory.UNLOCK_DATE))
            category = ETrophyMetadataCategory.METAL
        elif is_metal_next and is_metal_line(line):
            is_unlock_date_next = False
            category = ETrophyMetadataCategory.METAL

        if category is not None:
            output_file.write(process_line(line, category))
            is_name_next = category == ETrophyMetadataCategory.METAL
            is_criteria_next = category == ETrophyMetadataCategory.NAME
            is_unlock_date_next = category == ETrophyMetadataCategory.CRITERIA
            is_metal_next = category == ETrophyMetadataCategory.CRITERIA or category == ETrophyMetadataCategory.UNLOCK_DATE


def header():
    return 'name,criteria,unlocked,metal\n'


def process_line(line, category):
    def quote(s): return '"' + s + '"'

    if category == ETrophyMetadataCategory.UNLOCK_DATE:
        return quote(str(line is not None)) + ','
    elif category == ETrophyMetadataCategory.NAME:
        return quote(line.strip()) + ','
    elif category == ETrophyMetadataCategory.CRITERIA:
        return quote(line.strip()) + ','
    elif category == ETrophyMetadataCategory.METAL:
        return quote(line.strip().lower().capitalize()) + '\n'
    else:
        return ''


def is_unlock_date_line(line):
    MONTHS = [
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec'
    ]

    normalized = line.strip().lower().capitalize().replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
    components = normalized.split(' ')

    if len(components) != 3:
        return False

    day, month, year = components

    if int(day) < 1 or int(day) > 31:
        return False
    if month not in MONTHS:
        return False
    if int(year) < 2000:
        return False

    return True


def is_metal_line(line):
    normalized = line.strip().lower().capitalize()
    metals = allMetals()
    return normalized in metals


if __name__ == '__main__':
    input_path, output_path = parse_args()
    with open(input_path, 'r') as input_file:
        with open(output_path, 'w') as output_file:
            main(input_file, output_file)
