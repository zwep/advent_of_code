import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "11"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
# _ = helper.fetch_data(DAY)
# _ = helper.fetch_test_data(DAY)
#
# # read input
# puzzle_input = helper.read_lines_strip(DDATA_DAY)
# test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

def split(x: int):
    x_str = str(x)
    n = len(x_str)
    if x == 0:
        return [1]
    elif n % 2 == 0:
        return [int(x_str[:n//2]), int(x_str[n//2:])]
    else:
        return [x * 2024]


def run(x, n_count, counter=0):
    print(x, counter)
    if n_count == 0:
        return
    else:
        for i in split(x):
            counter += 1
            run(i, n_count - 1, counter)


run(7, 6)