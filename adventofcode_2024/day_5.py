import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def get_score(valid_updates):
    s = 0
    for valid_update in valid_updates:
        n = len(valid_update)
        if n % 2 == 1:
            n_mid = n // 2
            s += valid_update[n_mid]
        else:
            print("uhh")
    return s


DAY = "05"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = puzzle_input
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

valid_updates = []
invalid_updates = []
for update in updates:
    update_int = helper.int_str2list(update, sep=',')
    update_set = set(update_int)
    relevant_rules = []
    for i, rule_set in enumerate(rules_set):
        if len(rule_set.difference(update_set)) == 0:
            relevant_rules.append(rules_int[i])

    update_check = [update_int.index(x) < update_int.index(y) for x, y in relevant_rules]
    if all(update_check):
        valid_updates.append(update_int)
    else:
        invalid_updates.append((update_int, relevant_rules))

# Now select the middle pages
s = get_score(valid_updates)
print(s)

"""
part 2
"""

corrected_updates = []
for update_int, rules in invalid_updates:
    print(update_int)
    update_check = [update_int.index(x) < update_int.index(y) for x, y in rules]
    while not all(update_check):
        illegal = update_check.index(False)
        x, y = rules[illegal]
        ix = update_int.index(x)
        iy = update_int.index(y)
        update_int[ix], update_int[iy] = update_int[iy], update_int[ix]
        update_check = [update_int.index(x) < update_int.index(y) for x, y in rules]
        print(sum(update_check))
    corrected_updates.append(update_int)


s = get_score(corrected_updates)
print(s)