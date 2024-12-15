import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "13"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')
DDATA_CELINE = os.path.join(DDATA_YEAR, '13_celine.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)
# read input
puzzle_input = helper.read_lines_strip(DDATA_CELINE)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

def parse_puzzle(puzzle):
    problems = []
    problem = []
    for iline in puzzle:
        if iline != '':
            stepsize = re.findall("([0-9]+)", iline)
            stepsize = [int(x) for x in stepsize]
            problem.append(stepsize)
        else:
            problems.append(problem)
            problem = []
    problems.append(problem)

    return problems


def is_int(x, eps):
    if abs(x - np.round(x)) < eps:
        return True
    else:
        return False


cost_A = 3
cost_B = 1

modifier = 10000000000000
EPS = 1e-3
total = 0
problems = parse_puzzle(puzzle_input)
for problem in problems:
    A = np.array(problem[:2]).T
    b = np.array(problem[-1]) + modifier
    solution = np.linalg.inv(A.T @ A) @ A.T @ b
    if is_int(solution[0], EPS) and  is_int(solution[1], EPS):
        count_A = np.round(solution[0])
        count_B = np.round(solution[1])
        total += cost_A * count_A + cost_B * count_B

print(total)