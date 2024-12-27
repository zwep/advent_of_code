import numpy as np
import os
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "10"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data...
#_ = helper.fetch_data(DAY)
#_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

# find position
# start walking / making moves...
# return if we are at 9
#

chosen_puzzle = puzzle_input
AREA_MAP = [[int(x) for x in list(y)] for y in chosen_puzzle]

def validate_step_size(position, current_height):
    new_height = AREA_MAP[position[0]][position[1]]
    return (new_height - current_height) == 1

def get_trail_heads(position):
    ix, iy = position
    current_height = AREA_MAP[ix][iy]
    possible_moves = helper.get_moves(*position)
    possible_moves = [x for x in possible_moves if helper.validate_coordinate(x, len(AREA_MAP))]
    possible_moves = [x for x in possible_moves if validate_step_size(x, current_height)]
    trail_heads = 0
    for new_position in possible_moves:
        # I already know this
        new_height = AREA_MAP[new_position[0]][new_position[1]]
        if new_height == 9:
            #print('\t\t', trail_heads)
            trail_heads += 1
            if new_position not in TRAIL_HEAD_MAP:
                TRAIL_HEAD_MAP[new_position] = 1
        else:
            #print(new_height, new_position)
            trail_heads += get_trail_heads(new_position)

    return trail_heads

starting_positions = helper.find_positions(AREA_MAP, 0)

total = 0
for i_start in starting_positions:
    TRAIL_HEAD_MAP = {}
    temp = get_trail_heads(i_start)
    total += temp #len(TRAIL_HEAD_MAP)

print(total)