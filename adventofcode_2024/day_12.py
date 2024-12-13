import numpy as np
import os
import re
import matplotlib
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

chosen_puzzle = new_test_puzzle

chosen_puzzle = [list(x) for x in chosen_puzzle]
n = len(chosen_puzzle)

pools = {}
import itertools

# Get available moves
def get_moves(ix, iy):
    moves = [(ix - 1, iy), (ix + 1, iy), (ix, iy - 1), (ix, iy + 1)]
    return moves

index = {k: None for k in itertools.product(range(n), range(n))}
index_boundary = {}
positions = list(index.keys())
group_number = 0
while len(positions):
    # print("Group number ", group_number)
    position = positions.pop()
    # print("Position ", position)
    ix, iy = position
    garden_tile = chosen_puzzle[ix][iy]
    index[position] = (group_number, garden_tile)
    neighbours = get_moves(*position)
    # print("Neighbours ", len(neighbours), neighbours, index_boundary.get(group_number))
    # Do add their fences
    for x in neighbours:
        if not helper.validate_coordinate(x, n):
            # index_boundary.setdefault(group_number, 0)
            # index_boundary[group_number] += 1
            index_boundary.setdefault(group_number, [])
            index_boundary[group_number].append(x)
        if index.get(x) is not None:
            if index.get(x)[0] != group_number:
                # index_boundary.setdefault(group_number, 0)
                # index_boundary[group_number] += 1
                index_boundary.setdefault(group_number, [])
                index_boundary[group_number].append(x)

    # Now remove them
    neighbours = [x for x in neighbours if index.get(x, -1) is None]
    # print("Neighbours ", len(neighbours), neighbours, index_boundary.get(group_number))
    while len(neighbours):
        neighbour = neighbours.pop()
        # print("\tNeighbour ", neighbour)
        jx, jy = neighbour
        other_garden_tile = chosen_puzzle[jx][jy]
        if garden_tile == other_garden_tile:
            # print("\tIs in Yes", index_boundary.get(group_number))
            # Administration...
            index_neighbour = positions.index(neighbour)
            _ = positions.pop(index_neighbour)
            index[neighbour] = (group_number, garden_tile)
            new_neighbours = get_moves(*neighbour)
            # print("New neighbours ", len(new_neighbours), new_neighbours, index_boundary.get(group_number))
            # Do add their fences
            for x in new_neighbours:
                if not helper.validate_coordinate(x, n):
                    # index_boundary.setdefault(group_number, 0)
                    # index_boundary[group_number] += 1
                    index_boundary.setdefault(group_number, [])
                    index_boundary[group_number].append(x)
                if index.get(x) is not None:
                    if index.get(x)[0] != group_number:
                        # index_boundary.setdefault(group_number, 0)
                        # index_boundary[group_number] += 1
                        index_boundary.setdefault(group_number, [])
                        index_boundary[group_number].append(x)
            neighbours.extend(new_neighbours)
            neighbours = [x for x in neighbours if index.get(x, -1) is None]
            # print("New neighbours ", len(neighbours), neighbours, index_boundary.get(group_number))
        else:
            index_boundary.setdefault(group_number, [])
            index_boundary[group_number].append(neighbour)
            # index_boundary.setdefault(group_number, 0)
            # index_boundary[group_number] += 1
            # print("\tIs in: No, ", index_boundary.get(group_number))
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

new_stuff_thingy = {}
for sel_group in index_boundary.keys():
    sel_group = 0
    index_2 = {k: None for k in set(index_boundary[sel_group])}
    positions_2 = list(index_2.keys())
    group_number_2 = 0
    for x, y in positions_2:
        plt.scatter(x,y)
    plt.show(block=True)
    while len(positions_2):
        #print("Group number ", group_number)
        position_2 = positions_2.pop()
        index_2[position_2] = (group_number_2, None)
        neighbours_2 = get_moves(*position_2)
        neighbours_2 = [x for x in neighbours_2 if index_2.get(x, -1) is None]
       # print("Neighbours ", len(neighbours), neighbours)
        while len(neighbours_2):
            neighbour_2 = neighbours_2.pop()
            #print("\tNeighbour ", neighbour)
            jx, jy = neighbour_2
            if neighbour_2 in index_2:
                # Administration...
                index_neighbour_2 = positions_2.index(neighbour_2)
                _ = positions_2.pop(index_neighbour_2)
                index_2[neighbour_2] = (group_number_2, None)
                new_neighbours_2 = get_moves(*neighbour_2)

                neighbours_2.extend(new_neighbours_2)
                neighbours_2 = [x for x in neighbours_2 if index_2.get(x, -1) is None]
                #print("New neighbours ", len(neighbours), neighbours)

        else:
            group_number_2 += 1

    print(sel_group, result[sel_group][0], group_number_2)
    new_stuff_thingy[sel_group] = group_number_2

print(new_stuff_thingy)