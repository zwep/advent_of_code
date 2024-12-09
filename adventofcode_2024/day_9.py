import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "09"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

# ik wil weten op welke index de files staan... en met welke waarde

chosen_puzzle = test_puzzle_input
chosen_puzzle = list(chosen_puzzle[0])

file_blocks = [int(x) for x in chosen_puzzle[::2]]
ID_file_blocks = [str(x) for x in range(0, len(chosen_puzzle[::2]))]
free_space = [int(x) for x in chosen_puzzle[1::2]]

index_free_space = []
n = len(free_space)
for i in range(n):
    file_block = file_blocks[i]
    if i > 0:
        last_pos = index_free_space[-1] + 1
    else:
        last_pos = 0

    for j in range(free_space[i]):
        new_pos = file_block + last_pos + j
        index_free_space.append(new_pos)

file_blocks_derp = ''.join([x_size * x_ID for x_size, x_ID in zip(file_blocks, ID_file_blocks)])
# Oke let op...
# Indices kunnen groter dan 10 zijn.. dus deze methode werkt nog niet fantastisch
