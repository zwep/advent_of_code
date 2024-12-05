import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "05"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = test_puzzle_input
rules = []
updates = []
proces_rule = True
for item in chosen_puzzle:
    if proces_rule:
        rules.append(item)
    else:
        updates.append(item)

    if item == '':
        proces_rule = False

rules_int = [helper.int_str2list(x, sep="|") for x in rules if x]
rules_set = [set(x) for x in rules_int]

for update in updates:
    update_int = helper.int_str2list(update, sep=',')
    update_set = set(update_int)
