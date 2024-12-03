import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR
import collections

DAY = "01"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data
_ = helper.fetch_data(DAY)
# _ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
# test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

def diff(x):
    x = list(x)
    return abs(x[0] - x[1])

list_one, list_two = zip(*[map(int, x.split()) for x in puzzle_input])
sum([abs(x-y) for x,y in zip(sorted(list_one), sorted(list_two))])

occurences_one = collections.Counter(list_one)
occurences_two = collections.Counter(list_two)

s = 0
for k, v in occurences_one.items():
    s += v * (k * occurences_two.get(k, 0))
