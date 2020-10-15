import sys
import re
from os import getcwd
from os.path import join

from ETrophyMetadataCategory import ETrophyMetadataCategory
from ETrophyMetal import ETrophyMetal


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


def line_is_date(line):
    date_pattern = r'\d{1,2}(th|st|nd)\s*.{3}\s*20\d{2}'    
    return re.search(date_pattern, line) is not None


def line_is_time(line):
    time_pattern = r'\d{1,2}:\d{2}:\d{2}\s*(am|AM|pm|PM)'
    return re.search(time_pattern, line) is not None


def write_header_line(output_file):
    output_file.write('unlocked,missable,name,criteria,metal')


def write_data_line(data, output_file):
    unlocked = ETrophyMetadataCategory.UNLOCK_DATE in data  and ETrophyMetadataCategory.UNLOCK_TIME in data
    name = data[ETrophyMetadataCategory.NAME]
    criteria = data[ETrophyMetadataCategory.CRITERIA]
    metal = str(data[ETrophyMetadataCategory.METAL])

    output_line = f'{unlocked},{False},{name},{criteria},{metal}\n'
    output_file.write(output_line)


def main(input_file, output_file):
    # write_header_line(output_file)

    all_data = []

    current_data = dict()
    current_data_index = 0

    for line in input_file:
        category = ETrophyMetadataCategory(current_data_index)

        if category == ETrophyMetadataCategory.UNLOCK_DATE and not line_is_date(line):
            current_data_index += 1
            category = ETrophyMetadataCategory(current_data_index)
        
        if category == ETrophyMetadataCategory.UNLOCK_TIME and not line_is_time(line):
            current_data_index += 1
            category = ETrophyMetadataCategory(current_data_index)

        if category == ETrophyMetadataCategory.METAL:
            current_data[category] = ETrophyMetal.from_str(line.strip().replace(',', ''))
            all_data.append(current_data)
            current_data = dict()
            current_data_index = 0
        else:
            current_data[category] = line.strip().replace(',', '')
            current_data_index += 1
    
    ordered_data = sorted(all_data, reverse=True, key=lambda data: data[ETrophyMetadataCategory.METAL])
    for data in ordered_data:
        write_data_line(data, output_file)



if __name__ == '__main__':
    input_path, output_path = parse_args()
    with open(input_path, 'r') as input_file:
        with open(output_path, 'w') as output_file:
            main(input_file, output_file)
