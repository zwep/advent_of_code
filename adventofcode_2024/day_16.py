import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "16"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = test_puzzle_input
start_position = helper.find_position(chosen_puzzle, 'S')
end_position = helper.find_position(chosen_puzzle, 'E')

upper_bound = len(chosen_puzzle[0])

def validate_coordinate(x, prev_direction, upper_bound, puzzle):
    # Maybe filter on going backwards...?
    no_backsies = x[0] != helper.STEP2REV.get(prev_direction)
    correct_tile = puzzle[x[0]][x[1]] != '#'
    in_bounds = helper.validate_coordinate(x, upper_bound=upper_bound)
    return no_backsies and correct_tile and in_bounds


def get_valid_neighbours(position, prev_direction, upper_bound, puzzle):
    neighbours = helper.get_dir_and_moves(*position)
    return [x for x in neighbours if validate_coordinate(x[1], prev_direction=prev_direction,
                                                         upper_bound=upper_bound, puzzle=puzzle)]


# if prev_direction != direction --> cost + 1000?
to_visit = [start_position]
prev_direction = None
cost = {}

while len(to_visit):
    next_position = to_visit.pop()
    neighbours = get_valid_neighbours(next_position, prev_direction, upper_bound, chosen_puzzle)
    for step_dir, neighbour in neighbours:
        if step_dir == prev_direction:
            cost = 1
        else:
            cost = 1000
        prev_direction = step_dir
