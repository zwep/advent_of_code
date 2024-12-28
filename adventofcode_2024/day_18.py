import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "18"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)


def validate_coordinate(position, upper_bound, puzzle):
    in_bounds = helper.validate_coordinate(position, upper_bound=upper_bound)
    if not in_bounds:
        return False

    correct_tile = puzzle[position[0]][position[1]] != '#'
    return correct_tile and in_bounds


def get_valid_neighbours(position, upper_bound, puzzle):
    ix, iy = position
    neighbours = helper.get_moves(ix, iy)
    # Validate the positions
    return [x for x in neighbours if validate_coordinate(x, upper_bound=upper_bound, puzzle=puzzle)]


def parse_puzzle(puzzle, N):
    area_map = np.zeros((N,N), dtype=str)
    for i in puzzle:
        a, b = i.split(",")
        a = int(a)
        b = int(b)
        if b>= N or a >= N:
            print(a,b)

        area_map[a,b] = "#"
    area_map[area_map == ''] = '.'
    return area_map

N = 71
start_position = (0,0)
end_position = (N-1,N-1)

for II in range(1024, len(puzzle_input)):
    chosen_puzzle = puzzle_input[:(II-1)]
    area_map = parse_puzzle(chosen_puzzle, N)

    MAX_DIST = int(1e10)
    # Initialize the cost dicitonary
    possible_positions = helper.find_positions(area_map, '.')
    cost = {}
    previous = {}
    for k in possible_positions + [start_position, end_position]:
        cost.update({k : MAX_DIST})
        previous.update({k: []})

    # Precompute these, will probably speed up stuff: not that much
    neighbour_search = {}
    for i_pos, _ in cost.items():
        neighbours = get_valid_neighbours(i_pos, N, area_map)
        neighbour_search[i_pos] = neighbours

    # Initialize the to_visit list
    # to_visit = set(cost.keys())
    cost[start_position] = 0
    visited = set()
    to_visit = set()
    to_visit.add(start_position)

    while len(to_visit):
        print(len(to_visit), end='\r')
        min_cost, position = min([(cost[x], x) for x in to_visit], key=lambda x: x[0])
        if min_cost == MAX_DIST:
            break

        neighbours = neighbour_search[position]
        neighbours = [x for x in neighbours if x not in visited]
        for neighbour in neighbours:
            current_cost = 1
            # Store both the direction and the neighbor number in there
            if neighbour in cost:
                # Take the minimum between the cost that we know and the new cost
                cost[neighbour] = min(cost[neighbour], current_cost + cost[position])
                previous[neighbour].append(position)
            else:
                cost.setdefault(neighbour, current_cost + cost[position])

            if neighbour in visited:
                continue

            to_visit.add(neighbour)
        to_visit.remove(position)
        visited.add(position)

    if cost[end_position] == MAX_DIST:
        print('Cant reach', chosen_puzzle[-1])
        break
    #print('cost final position: ',cost[end_position])

