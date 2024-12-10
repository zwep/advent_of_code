from copy import deepcopy

import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR

import itertools
import collections

DAY = "09"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)
test_puzzle_input = test_puzzle_input[0]

chosen_puzzle = test_puzzle_input

file_blocks = [int(x) for x in chosen_puzzle[::2]]
free_space = [int(x) for x in chosen_puzzle[1::2]]

index_free_space = []
n = len(free_space)
memory = 0
for i in range(n):
    file_block = file_blocks[i]
    if len(index_free_space):
        last_pos = index_free_space[-1] + 1 + memory
    else:
        last_pos = memory

    if free_space[i] == 0:
        memory += file_block
    else:
        memory = 0
        for j in range(free_space[i]):
            new_pos = file_block + last_pos + j
            index_free_space.append(new_pos)

file_blocks_explicit = list(itertools.chain(*[size * [ID] for ID, size in enumerate(file_blocks)]))

"""
Part 1
"""

for i_loc in index_free_space:
    x = file_blocks_explicit.pop()
    file_blocks_explicit.insert(i_loc, x)

print(sum([int(x) * i for i, x in enumerate(file_blocks_explicit)]))

# calculate score...
# 6104973916432 -- too low
# 6200703828680 -- too low
# 6211348208140 -- yes

"""
Part 2
"""

test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)
test_puzzle_input = test_puzzle_input[0]
chosen_puzzle = test_puzzle_input

file_blocks = [int(x) for x in chosen_puzzle[::2]]
# file_blocks_explicit = list(itertools.chain(*[size * [ID] for ID, size in enumerate(file_blocks)]))

free_space = [int(x) for x in chosen_puzzle[1::2]]
# index_free_spaces = [[None for _ in range(free_space[i])] for i in range(len(free_space))]
index_free_spaces = [[] for i in range(len(free_space))]

filled_space = [None for i in range(len(file_blocks))]
# Get the size of the file block
while len(file_blocks) > 0:
    index_file_block = len(file_blocks) - 1
    n_file_block = file_blocks.pop()
    print('Name: ', index_file_block)
    print('Size: ', n_file_block)
    # # Remove the items from the explicit file block
    # file_block = [file_blocks_explicit.pop() for _ in range(n_file_block)]
    # Get the first fitting free space
    potential_index_free_space = [i for i,x in enumerate(free_space[:index_file_block]) if x >= n_file_block]
    print('Potential free: ', potential_index_free_space)
    if len(potential_index_free_space) == 0:
        # It doesnt move
        filled_space[index_file_block] = True
        continue
    else:
        filled_space[index_file_block] = False
        index_free_space = potential_index_free_space[0]
    print('\t Chose: ', index_free_space)
    # Update the size of the free space left
    n_free_space = free_space[index_free_space]
    # index_free_spaces[index_free_space][-n_free_space:(-n_free_space + n_file_block)] = n_file_block * [index_file_block]
    index_free_spaces[index_free_space].extend(n_file_block * [index_file_block])
    free_space[index_free_space] -= n_file_block

for i in range(len(free_space)):
    n_left_over = free_space[i]
    if n_left_over == 0:
        continue

    index_free_spaces[i].extend([None] * n_left_over)

# Calculate score...
file_blocks = [int(x) for x in chosen_puzzle[::2]]
free_space = [int(x) for x in chosen_puzzle[1::2]]

s = 0
for i, filled in enumerate(filled_space):
    if filled:
        n_size = file_blocks[i]
        # deze i hier klopt niet.
        index_file_block = i
        if i > 0:
            index_file_block += free_space[i-1]
        print(index_file_block, n_size)
        contribution = sum([index_file_block * j for j in range(n_size)])
        s += contribution

    index_free_spaces[i]