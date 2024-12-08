import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR

import re
import itertools

DAY = "07"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)


def get_content(equation):
    answer, components = equation.split(":")
    components = helper.int_str2list(components.strip(), sep=" ")
    return components, int(answer)

def check_equation(components, answer):
    n = len(components)
    combinations = itertools.product(["*", "+", "||"], repeat=n - 1)
    for combination in combinations:
        total = components[0]
        for operator, x in zip(combination, components[1:]):
            if operator == "||":
                total = int(str(total) + str(x))
            else:
                total = eval(f"{total}{operator}{x}")
            if total > answer:
                break
        if total == answer:
            return answer
    else:
        return 0


chosen_puzzle = puzzle_input
result = []
for ii, equation in enumerate(chosen_puzzle):
    print(ii, end='\r')
    result.append(check_equation(*get_content(equation)))

sum(result)

# haakt op