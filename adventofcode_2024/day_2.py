import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def diff(x: list):
    return [x - y for x, y in zip(x[1:], x[:-1])]


def get_asc(x: list):
    return [y > 0 for y in diff(x)]


def is_asc(x: list):
    return all(get_asc(x))

def get_desc(x: list):
    return [y < 0 for y in diff(x)]

def is_desc(x: list):
    return all(get_desc(x))

def get_safe(x: list, safety_level=3):
    return [1 <= abs(y) <= safety_level for y in diff(x)]

def is_safe(x: list, safety_level=3):
    return all(get_safe(x, safety_level=safety_level))


def is_asc_relax(x: list, z=1):
    return sum(get_asc(x)) == (len(x) - z)


def is_desc_relax(x: list, z=1):
    return sum(get_desc(x)) == (len(x) - z)



DAY = "02"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data...
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip_split_to_int(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip_split_to_int(DDATA_DAY_TEST)


result_part_1 =[is_safe(x) for x in puzzle_input if is_desc(x) or is_asc(x)]
print("Part 1", sum(result_part_1))

"""
Part 2

We have one relaxation... either in descending/ascending or when we check for safety
So we get...

total number
    total desc OK    -- safe?
                    -- safe relaxed?
    total desc relaxed -- safe?
    
    total asc OK   -- safe?
                    -- safe relaxed?
    total asc relaxed -- safe?
"""

chosen_puzzle = puzzle_input
# chosen_puzzle = [[1,3,4,1,2,3]]
n_safe = 0
count = 0
n_unsafe = 0
#
# chosen_puzzle = [[1, 4, 7, 10],
#                  [10, 7, 4, 1],
#                  [1, 4, 7, 6, 13, 16],
#                  [16, 13, 6, 7, 4, 1],
#                  [1, 4, 7, 14, 10, 13],
#                  [16, 13, 14, 7, 4, 1]]

for i_x in chosen_puzzle:
    print("---------------------")
    print(i_x)
    if is_asc(i_x):
        print("Ascending ")
        if is_safe(i_x):
            n_safe += 1
            print("safe")
        else:
            deviation = get_safe(i_x)
            false_index = deviation.index(False)
            x_01 = i_x[:false_index] + i_x[false_index + 1:]
            x_02 = i_x[:false_index + 1] + i_x[false_index + 1 + 1:]
            if is_safe(x_01) or is_safe(x_02):
                n_safe += 1
                print("safe")
            else:
                n_unsafe += 1
                print("not safe")
        continue
    elif is_desc(i_x):
        print("Descending ")
        if is_safe(i_x):
            n_safe += 1
            print("safe")
        else:
            deviation = get_safe(i_x)
            false_index = deviation.index(False)
            x_01 = i_x[:false_index] + i_x[false_index + 1:]
            x_02 = i_x[:false_index + 1] + i_x[false_index + 1 + 1:]
            if is_safe(x_01) or is_safe(x_02):
                n_safe += 1
                print("safe")
            else:
                n_unsafe += 1
                print("not safe")
        continue

    elif is_asc_relax(i_x, 2):
        print("Ascending relax ")
        x_diff = get_asc(i_x)
        false_index = x_diff.index(False)
        x_01 = i_x[:false_index] + i_x[false_index + 1:]
        x_02 = i_x[:false_index + 1] + i_x[false_index + 1 + 1:]
        if (is_asc(x_01) and is_safe(x_01)) or (is_asc(x_02) and is_safe(x_02)):
            n_safe += 1
            print("safe")
        else:
            n_unsafe += 1
            print("not safe")
        continue

    elif is_desc_relax(i_x, 2):
        print("Descending relax ")
        x_diff = get_desc(i_x)
        false_index = x_diff.index(False)
        x_01 = i_x[:false_index] + i_x[false_index + 1:]
        x_02 = i_x[:false_index + 1] + i_x[false_index + 1 + 1:]
        if (is_desc(x_01) and is_safe(x_01)) or (is_desc(x_02) and is_safe(x_02)):
            n_safe += 1
            print("safe")
        else:
            n_unsafe += 1
            print("not safe")
        continue
    count += 1

print(n_safe, n_unsafe, count)

# 489 too high
# 479 too low