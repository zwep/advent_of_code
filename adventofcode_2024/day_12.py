import numpy as np
import os
import re
import matplotlib

from adventofcode_2020.day4 import string_dicts

matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR

DAY = "12"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

new_test_puzzle = ["RRRRIICCFF",
"RRRRIICCCF",
"VVRRRCCFFF",
"VVRCCCJFFF",
"VVVVCJJCFE",
"VVIVCCJJEE",
"VVIIICJJEE",
"MIIIIIJJEE",
"MIIISIJEEE",
"MMMISSJEEE"]

chosen_puzzle = puzzle_input

chosen_puzzle = [list(x) for x in chosen_puzzle]
n = len(chosen_puzzle)

pools = {}
import itertools


index = {k: None for k in itertools.product(range(n), range(n))}
index_boundary = {}
positions = list(index.keys())
group_number = 0
while len(positions):
    #print("Group number ", group_number)
    position = positions.pop()
    # print("Position ", position)
    ix, iy = position
    garden_tile = chosen_puzzle[ix][iy]
    index[position] = (group_number, garden_tile)
    neighbours = helper.get_moves(*position)

    while len(neighbours):
        step_dir, neighbour = neighbours.pop()
        # print("\tNeighbour ", neighbour, len(index_boundary.get(group_number, [])))
        if not helper.validate_coordinate(neighbour, n):
            # print("\t\tNot valid")
            index_boundary.setdefault(group_number, [])
            index_boundary[group_number].append((step_dir, neighbour))
            continue

        if index.get(neighbour) is not None:
            # print("\t\tAlready in index")
            if index.get(neighbour)[0] != group_number:
                # print("\t\t\tDifferent group")
                index_boundary.setdefault(group_number, [])
                index_boundary[group_number].append((step_dir, neighbour))

            continue

        jx, jy = neighbour
        other_garden_tile = chosen_puzzle[jx][jy]
        if garden_tile == other_garden_tile:
            # print("\t\tSame tile")
            # Administration...
            index_neighbour = positions.index(neighbour)
            _ = positions.pop(index_neighbour)
            index[neighbour] = (group_number, garden_tile)
            new_neighbours = helper.get_moves(*neighbour)
            neighbours.extend(new_neighbours)
        else:
            # print("\t\tDifferent tile")
            index_boundary.setdefault(group_number, [])
            index_boundary[group_number].append((step_dir, neighbour))
    else:
        group_number += 1


index_boundary
result = [[v[1] for k, v in index.items() if v[0] == i] for i in range(group_number)]
s = 0
for i, x in enumerate(result):
    t = len(x) * len(index_boundary[i])
    print(x[0], t)
    s +=t

print(s)

"""
Now... how to get the sides..

This didnt work

Because Im not counting certain things double neough
"""

final_result = {}
for sel_group in index_boundary.keys():
    sel_boundary = index_boundary[sel_group]
    final_result.setdefault(sel_group, 0)
    s = 0
    for step_dir, step in helper.STEP2POS.items():
        print(step_dir)
        step_filter_boundary = [x[1] for x in sel_boundary if x[0] == step_dir]
        if step_dir in ['L', 'R']:
            # This should be OK for L/R step_dirs
            min_y = min(step_filter_boundary, key=lambda x: x[1])[1]
            max_y = max(step_filter_boundary, key=lambda x: x[1])[1]

            for iy in range(min_y, max_y+1):
                filter_boundary = sorted([x[0] for x in step_filter_boundary if x[1] == iy])
                # print(filter_boundary)
                if len(filter_boundary) == 0:
                    continue

                difflist = helper.difference_element_list(filter_boundary)
                size = len([x for x in difflist if x != 1]) + 1
                s += size
        else:
            # This should be OK for U/D step_dirs
            min_x = min(step_filter_boundary, key=lambda x: x[0])[0]
            max_x = max(step_filter_boundary, key=lambda x: x[0])[0]

            for ix in range(min_x, max_x + 1):
                filter_boundary = sorted([x[1] for x in step_filter_boundary if x[0] == ix])
                # print(filter_boundary)
                if len(filter_boundary) == 0:
                    continue

                difflist = helper.difference_element_list(filter_boundary)
                size = len([x for x in difflist if x != 1]) + 1
                s += size

    final_result[sel_group] = s * len(result[sel_group])

finak_s = 0
for k, v in final_result.items():
    print(result[k][0], v)
    finak_s += v
