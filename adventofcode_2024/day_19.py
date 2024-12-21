import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "19"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

def parse_puzzel(puzzle):
    split_index = puzzle.index('')
    towel_patterns = puzzle[:split_index]
    towel_designs = puzzle[split_index+1:]
    # Split into parts...
    towel_patterns = towel_patterns[0].split(", ")
    towel_designs = [list(x) for x in towel_designs]
    return towel_patterns, towel_designs


def check_design(towel_design):
    towel_design_str = ''.join(towel_design)
    if towel_design_str in knowledge_is_power:
        return knowledge_is_power[towel_design_str]

    global towel_patterns
    possible_patterns = [x for x in towel_patterns if x == ''.join(towel_design[:len(x)])]
    fitting_pattern = 0
    for possible_pattern in possible_patterns:
        if len(possible_pattern) == len(towel_design):
            fitting_pattern += 1
        else:
            fitting_pattern += check_design(towel_design[len(possible_pattern):])

    knowledge_is_power[towel_design_str] = fitting_pattern
    return fitting_pattern

chosen_puzzle = puzzle_input
knowledge_is_power = {}
towel_patterns, towel_designs = parse_puzzel(chosen_puzzle)
total = 0
while len(towel_designs):
    towel_design = towel_designs.pop()
    result = check_design(towel_design)
    # print(towel_design, result)
    total += result

print(total)