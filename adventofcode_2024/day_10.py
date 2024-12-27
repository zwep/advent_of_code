import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "10"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

def process_position(position):
    ix, iy = position
    print(position)
    current_level = area_map[ix][iy]
    possible_levels = []
    for x in helper.get_moves(ix, iy):
        if helper.validate_coordinate(x, len(area_map)):
            print(x)
            if (area_map[x[0]][x[1]] - current_level) == 1:
                possible_levels.append((area_map[x[0]][x[1]], x))
    possible_trails = 0
    for level, step in possible_levels:
        if level == 9:
            possible_trails += 1
        else:
            new_position = helper.update_position(position, step)
            print(position, step, new_position)
            process_position(new_position)

    return possible_trails

chosen_puzzle = test_puzzle_input
area_map = [[int(x) for x in y] for y in chosen_puzzle]
starting_positions = helper.find_positions(area_map, 0)
for start_position in starting_positions:
    z = process_position(start_position)
    print(z)