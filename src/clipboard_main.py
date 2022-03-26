import sys
import pyperclip

import trophies_processor
import trophy_formatter


def looks_like_trophy_input(str_input: str) -> bool:
    has_platinum = 'Platinum' in str_input
    has_gold = 'Gold' in str_input
    has_silver = 'Silver' in str_input
    has_bronze = 'Bronze' in str_input
    has_rarity = 'COMMON' in str_input or 'RARE' in str_input
    return has_bronze and has_silver and has_gold and has_platinum and has_rarity


def clipboard_main():
    clipboard_input = str(pyperclip.paste())

    if clipboard_input is None or clipboard_input == '':
        sys.exit('Error: Expected clipboard input. Clipboard is empty.')

    if not looks_like_trophy_input(clipboard_input):
        sys.exit('Error: Clipbard input doesn\'t look like Trophy data.')

    input_lines = [
        line.strip().replace('\t', '')
        for line
        in clipboard_input.split('\n')
        if line is not None and line.strip() != ''
    ]

    if len(input_lines) < 2:
        sys.exit('Error: Expected multiple lines of clipboard input')

    trophy_list = trophies_processor.process(input_lines)
    ouput = '\n'.join([trophy_formatter.csv(trophy) for trophy in trophy_list])

    print(ouput)
    pyperclip.copy(ouput)


if __name__ == '__main__':
    clipboard_main()
