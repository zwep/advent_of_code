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
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

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
MAX_DIST = int(1e10)
# Initialize the cost dicitonary
possible_positions = helper.find_positions(chosen_puzzle, '.')
cost = {}
previous = {}
for k in possible_positions + [start_position, end_position]:
    for i_dir in ['L', 'R', 'U', 'D']:
        cost.update({(i_dir, k) : MAX_DIST})
        previous.update({(i_dir, k): []})

# Precompute these, will probably speed up stuff: not that much
neighbour_search = {}
for k, _ in cost.items():
    i_dir, i_pos = k
    neighbours = get_valid_neighbours(i_pos, i_dir, upper_bound, chosen_puzzle)
    neighbour_search[k] = neighbours

# Initialize the to_visit list
# to_visit = set(cost.keys())
cost[('R', start_position)] = 0
visited = set()
to_visit = set()
to_visit.add(('R', start_position))

while len(to_visit):
    print(len(to_visit), end='\r')
    min_cost, (direction, position) = min([(cost[x], x) for x in to_visit], key=lambda x: x[0])
    # min_cost = cost[(direction, position)]
    if min_cost == MAX_DIST:
        break

    neighbours = neighbour_search[(direction, position)]
    neighbours = [x for x in neighbours if x not in visited]
    for step_dir, neighbour in neighbours:
        if step_dir == direction:
            current_cost = 1
        else:
            current_cost = 1000

        # Store both the direction and the neighbor number in there
        if (step_dir, neighbour) in cost:
            # Take the minimum between the cost that we know and the new cost
            cost[(step_dir, neighbour)] = min(cost[(step_dir, neighbour)], current_cost + cost[(direction, position)])
            previous[(step_dir, neighbour)].append((direction, position))
        else:
            cost.setdefault((step_dir, neighbour), current_cost + cost[(direction, position)])

        if (step_dir, neighbour) in visited:
            continue

        to_visit.add((step_dir, neighbour))
    to_visit.remove((direction, position))
    visited.add((direction, position))

end_dir, min_cost = min([(x, cost.get((x, end_position))) for x in helper.STEPS],key=lambda x: x[1])
print(end_dir, min_cost)


eehm = set()
to_look_after = [(end_dir, end_position)]
while len(to_look_after):
    temp_dir, temp_pos = to_look_after.pop()
    if temp_pos not in eehm:
        eehm.add(temp_pos)
    to_look_after.extend(previous[(temp_dir, temp_pos)])

len(eehm)
