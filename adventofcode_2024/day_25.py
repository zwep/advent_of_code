import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "25"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
# _ = helper.fetch_data(DAY)
# _ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

def parse_puzzle(puzzle):
    locks = []
    keys = []
    while '' in puzzle:
        split_index = puzzle.index('')
        lock_or_key = puzzle[:split_index]
        puzzle = puzzle[split_index+1:]
        if all([x == '#' for x in lock_or_key[0]]):
            locks.append(lock_or_key)
        else:
            keys.append(lock_or_key)

    # print(len(puzzle))
    # if all([x == '#' for x in puzzle[0]]):
    #     locks.append(puzzle)
    # else:
    #     keys.append(puzzle)

    return locks, keys


def count_pound_sign(x):
    n_column = len(x[0])
    counts = []
    for i in range(n_column):
        count = helper.get_column(x, i).count("#")
        counts.append(count-1)
    return counts


chosen_puzzle = puzzle_input
locks, keys = parse_puzzle(chosen_puzzle)

locks_count = [count_pound_sign(x) for x in locks]
keys_count = [count_pound_sign(x) for x in keys]

fit = 0
for i_lock in locks_count:
    for i_key in keys_count:
        check = [x + y <= 5 for x, y in zip(i_lock, i_key)]
        if all(check):
            fit += 1

print(fit)