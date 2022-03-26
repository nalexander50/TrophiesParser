from typing import Tuple

import sys
import os

import trophies_processor
import trophy_formatter


def parse_args() -> Tuple[str, str]:
    input_path = os.path.join(os.getcwd(), 'input.txt')
    output_path = os.path.join(os.getcwd(), 'output.csv')

    if len(sys.argv) >= 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    return (input_path, output_path)


def main(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf8') as input_file:
        trophy_list = trophies_processor.process(input_file.readlines())
        ouput = [trophy_formatter.csv(trophy) for trophy in trophy_list]

        with open(output_path, 'w', encoding='utf8') as output_file:
            output_file.writelines(ouput)


if __name__ == '__main__':
    arg_input_path, arg_output_path = parse_args()
    main(arg_input_path, arg_output_path)
