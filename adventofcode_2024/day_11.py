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
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

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
    print("\t"*counter,x, (10 - len(str(x))) * " ",  )
    if n_count == 0:
        return
    else:
        counter += 1
        for i in split(x):
            run(i, n_count - 1, counter)


# run(7, 25)

"""
Here we start with re-creating part 1...
"""

class Stone:
    def __init__(self, n_time):
        self.n_time = n_time
        # self.leaf_nodes = []
        self.collection = {}

    def run(self, x, n_count=None):
        if n_count is None:
            n_count = self.n_time

        if n_count == 0:
            return 1

        if (x, n_count) in self.collection.keys():
            return self.collection[(x, n_count)]

        result = 0
        for i in split(x):
            result += self.run(i, n_count - 1)

        self.collection[(x, n_count)] = result  # Memoize the result
        return result



test_puzzle_input = helper.int_str2list(puzzle_input[0], sep=' ')

n_total = 75
stone = Stone(n_total)
for x in test_puzzle_input:
    print("----", x)
    stone.run(x)


sum([stone.collection[(x, n_total)] for x in test_puzzle_input])


"""
Part 2
"""



