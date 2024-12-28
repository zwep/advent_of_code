import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def validate_coordinate(position, bounds, puzzle):
    in_bounds = helper.validate_coordinate(position, *bounds)
    if not in_bounds:
        return False

    correct_tile = puzzle[position[0]][position[1]] != '#'
    return correct_tile and in_bounds


def get_valid_neighbours(position, bounds, puzzle):
    ix, iy = position
    neighbours = helper.get_moves(ix, iy)
    # Validate the positions
    return [x for x in neighbours if validate_coordinate(x, bounds=bounds, puzzle=puzzle)]


def get_cheat_positions(area_map):
    # Find all positions that have the following pattern: .#. (or transposed)
    wall_positions = helper.find_positions(area_map, '#')
    posible_cheat_positions = []
    for wall_position in wall_positions:
        up = helper.update_position(wall_position, helper.STEP2POS['U'])
        down = helper.update_position(wall_position, helper.STEP2POS['D'])
        left = helper.update_position(wall_position, helper.STEP2POS['R'])
        right = helper.update_position(wall_position, helper.STEP2POS['L'])
        if helper.validate_coordinate(up, N, M) and helper.validate_coordinate(down, N, M):
            up_value = area_map[up[0]][up[1]]
            down_value = area_map[down[0]][down[1]]
            if up_value != '#' and down_value != '#':
                posible_cheat_positions.append(wall_position)
        if helper.validate_coordinate(left, N, M) and helper.validate_coordinate(right, N, M):
            left_value = area_map[left[0]][left[1]]
            right_value = area_map[right[0]][right[1]]
            if left_value != '#' and right_value != '#':
                posible_cheat_positions.append(wall_position)

    return posible_cheat_positions

def get_time(area_map, cheat_position):
    if cheat_position is not None:
        area_map[cheat_position[0]][cheat_position[1]] = '.'
    start_position = helper.find_position(area_map, 'S')
    end_position = helper.find_position(area_map, 'E')

    MAX_DIST = int(1e10)
    # Initialize the cost dicitonary
    possible_positions = helper.find_positions(area_map, '.')
    cost = {}
    previous = {}
    for k in possible_positions + [start_position, end_position]:
        cost.update({k: MAX_DIST})
        previous.update({k: []})

    # Precompute these, will probably speed up stuff: not that much
    neighbour_search = {}
    for i_pos, _ in cost.items():
        neighbours = get_valid_neighbours(i_pos, (N, M), area_map)
        neighbour_search[i_pos] = neighbours

    # Initialize the to_visit list
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
    return cost


def get_advantage(position, costs):
    up = tuple(helper.update_position(position, helper.STEP2POS['U']))
    down = tuple(helper.update_position(position, helper.STEP2POS['D']))
    left = tuple(helper.update_position(position, helper.STEP2POS['R']))
    right = tuple(helper.update_position(position, helper.STEP2POS['L']))
    potential_win_ud = potential_win_lr = 0
    if up in costs and down in costs:
        up_value = costs[up]
        down_value = costs[down]
        potential_win_ud = abs(up_value - down_value) - 2
    if left in costs and right in costs:
        left_value = costs[left]
        right_value = costs[right]
        potential_win_lr = abs(left_value - right_value)  - 2

    return max(potential_win_ud, potential_win_lr)

DAY = "20"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = puzzle_input
area_map = chosen_puzzle
area_map = [list(x) for x in area_map]

N = len(area_map)
M = len(area_map[0])

timings = {}
base_line_costs = {}
import copy
z = None
win_count = 0
cheat_positions = get_cheat_positions(area_map)
for ii, cheat_position in enumerate([None] + cheat_positions):
    print(ii, end='\r')
    area_map_copy = copy.deepcopy(area_map)
    if cheat_position is not None:
        z = get_advantage(cheat_position, base_line_costs)
        if z >= 100:
            win_count += 1
        continue

    end_position = helper.find_position(area_map, 'E')
    total_cost = get_time(area_map_copy, cheat_position)
    timings[cheat_position] = total_cost[end_position]
    if cheat_position is None:
        base_line_costs.update(total_cost)

    print(z, timings[None] - timings[cheat_position])

"""
Kay.. Part 2

From every position in the cost matrix with a "finite" cost
- Select all points that cost 100 less than the default case..? - Yeah something like this
- Check if they are within 20 positions
- ...
- profit..?

"""
