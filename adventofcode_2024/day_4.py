import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR
import scipy.signal


DAY = "04"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data...
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

xmas = list("XMAS")
convert = dict(zip(xmas, list(range(1, len(xmas) + 1))))

test_puzzle_input = helper.read_lines_strip_split_and_map(DDATA_DAY_TEST, converter=convert)
puzzle_input = helper.read_lines_strip_split_and_map(DDATA_DAY, converter=convert)

chosen_puzzle = puzzle_input

"""
Part 1
"""
kernel_line = [[1, 0, 0, 0], [10, 0, 0, 0], [100, 0, 0, 0], [1000, 0, 0, 0]]
kernel_diag = [[1, 0, 0, 0], [0, 10, 0, 0], [0, 0, 100, 0], [0, 0, 0, 1000]]
kernel_line = np.array(kernel_line)
kernel_diag = np.array(kernel_diag)

kernels_line = [kernel_line, kernel_line[::-1], kernel_line.T[:, ::-1], kernel_line.T]
kernels_diag = [kernel_diag, kernel_diag[::-1], kernel_diag[:, ::-1], kernel_diag[::-1, ::-1]]

A = np.array(chosen_puzzle)
s = 0
for kernel in kernels_line + kernels_diag:
    C = scipy.signal.convolve2d(A, kernel)
    C_disp = (C == 4321).astype(int)
    helper.print_binary(C_disp)
    s += np.sum(C_disp)

"""
Part 2
"""

xmas = list("XMAS")
convert = dict(zip(xmas, list(range(len(xmas)))))
puzzle_input = helper.read_lines_strip_split_and_map(DDATA_DAY, converter=convert)
test_puzzle_input = helper.read_lines_strip_split_and_map(DDATA_DAY_TEST, converter=convert)

chosen_puzzle = puzzle_input

kernel_cross = [[1, 0, 10], [0, 100, 0], [1000, 0, 10000]]
kernel_cross = np.array(kernel_cross)

kernels_crosses = [kernel_cross]

A = np.array(chosen_puzzle)
s = 0
identifiers = [31231, 13213, 33211, 11233]
for kernel in kernels_crosses:
    C = scipy.signal.convolve2d(A, kernel)
    for iid in identifiers:
        s += (C == iid).sum()

print(s)