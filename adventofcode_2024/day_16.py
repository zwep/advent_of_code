import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "16"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')
DDATA_DAY_TEST_2 = os.path.join(DDATA_YEAR, DAY + '_test_2.txt')

# Run get data..
#_ = helper.fetch_data(DAY)
#_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)
test_puzzle_input_2 = helper.read_lines_strip(DDATA_DAY_TEST_2)


def validate_coordinate(position, upper_bound, puzzle):
    correct_tile = puzzle[position[0]][position[1]] != '#'
    in_bounds = helper.validate_coordinate(position, upper_bound=upper_bound)
    return correct_tile and in_bounds


def get_valid_neighbours(position, direction, upper_bound, puzzle):
    step_in_direction = helper.STEP2POS[direction]
    new_position = helper.update_position(position, step_in_direction)
    # Create the neighbour that moves you in the same direction
    neighbour_01 = (direction, tuple(new_position))
    neighbours = [neighbour_01]
    # Create the rotated positions, these remain at the same node!
    forward_and_backward = set([direction, helper.STEP2REV[direction]])
    side_ways = helper.STEPS.difference(forward_and_backward)
    for i_direction in side_ways:
        neighbour = (i_direction, position)
        neighbours.append(neighbour)
    # Validate the positions
    return [x for x in neighbours if validate_coordinate(x[1], upper_bound=upper_bound, puzzle=puzzle)]


chosen_puzzle = puzzle_input
start_position = helper.find_position(chosen_puzzle, 'S')
end_position = helper.find_position(chosen_puzzle, 'E')

upper_bound = len(chosen_puzzle[0])

# Initialize the cost dicitonary
possible_positions = helper.find_positions(chosen_puzzle, '.')
cost = {}
for k in possible_positions + [start_position, end_position]:
    for i_dir in ['L', 'R', 'U', 'D']:
        cost.update({(i_dir, k) : int(1e10)})

# Precompute these, will probably speed up stuff: not that much
neighbour_search = {}
for k, _ in cost.items():
    i_dir, i_pos = k
    neighbours = get_valid_neighbours(i_pos, i_dir, upper_bound, chosen_puzzle)
    neighbour_search[k] = neighbours

# Initialize the to_visit list
to_visit = list(cost.keys())
cost[('R', start_position)] = 0
visited = []

while len(to_visit):
    print(len(to_visit), end='\r')
    mincost, (direction, position) = min([(cost[x], x) for x in to_visit])
    if mincost == 1e10:
        break
    index_position = to_visit.index((direction, position))
    _ = to_visit.pop(index_position)
    visited.append((direction, position))
    # print('In node ', direction, position, 'remaining to visit ', to_visit)
    neighbours = neighbour_search[(direction, position)]
    neighbours = [x for x in neighbours if x in to_visit]
    for step_dir, neighbour in neighbours:
        if step_dir == direction:
            current_cost = 1
        else:
            current_cost = 1000

        # print(direction, position, '-->', step_dir, neighbour, ': ', current_cost)
        # Store both the direction and the neighbor number in there
        if (step_dir, neighbour) in cost:
            # Take the minimum between the cost that we know and the new cost
            cost[(step_dir, neighbour)] = min(cost[(step_dir, neighbour)], current_cost + cost[(direction, position)])
        else:
            cost.setdefault((step_dir, neighbour), current_cost + cost[(direction, position)])

        if (step_dir, neighbour) in to_visit:
            continue

        if (step_dir, neighbour) in visited:
            continue
        # Only add when we are not already planning on visiting it
        # And when we have not already visited it
        to_visit.append((step_dir, neighbour))

min_cost = min([cost.get((x, end_position)) for x in helper.STEPS])
print(min_cost)
#
# 129468 -- too high
# 127520

#
# min_pos = min([(x, cost[(x, end_position)]) for x in helper.STEPS], key=lambda x: x[1])
# direction = min_pos[0]
#
# position = end_position
# import itertools
# while True:
#     z = [neighbour_search.get((x, position)) for x in helper.STEPS]
#     z = list(itertools.chain(*z))
#     z = list(set(z))
#     z_cost = [cost[x] for x in z]
#     min_cost = min(z_cost)
#     index_min = z_cost.index(min_cost)
#     position = z[index_min][1]
#     print(position, min_cost)
#
#     if helper.list_compare(position, start_position):
#         break
#
#
# [(x, cost.get((x, (2, 139)))) for x in helper.STEPS]

