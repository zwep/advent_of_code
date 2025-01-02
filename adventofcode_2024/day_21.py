import numpy as np
import os
import re
import itertools
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR
import itertools


def validate_position(position: tuple | list, area, bound_x, bound_y):
    in_bounds = helper.validate_coordinate(position, bound_x, bound_y)
    if not in_bounds:
        return False

    correct_tile = area[position[0]][position[1]] != '#'
    return correct_tile and in_bounds


def get_neighbours(position: tuple | list, area, bound_x, bound_y):
    ix, iy = position
    neighbours = helper.get_moves(ix, iy)
    return [x for x in neighbours if validate_position(x, area, bound_x, bound_y)]


def initialize_dijkstra(start_position, area, bound_x, bound_y):
    numeric_positions = [helper.find_positions(area, str(x)) for x in range(10)]
    A_position = [helper.find_positions(area, 'A')]
    arrow_postions = [helper.find_positions(area, str(x)) for x in helper.STEP2ARROW.values()]
    possible_positions = list(itertools.chain(*(numeric_positions + A_position + arrow_postions)))

    cost = {}
    previous = {}
    for k in possible_positions:
        cost.update({k: MAX_DIST})
        previous.update({k: []})

    neighbour_search = {}
    for i_pos in cost.keys():
        neighbours = get_neighbours(i_pos, area, bound_x, bound_y)
        neighbour_search[i_pos] = neighbours

    cost[start_position] = 0
    visited = set()
    to_visit = set()
    to_visit.add(start_position)

    return {"cost": cost,
            "previous": previous,
            "neighbours": neighbour_search,
            "visited": visited,
            "to_visit": to_visit,
            }


def run_dijkstra(initialized_components):
    cost = initialized_components["cost"]
    previous = initialized_components["previous"]
    neighbour_search = initialized_components["neighbours"]
    visited = initialized_components["visited"]
    to_visit = initialized_components["to_visit"]
    while len(to_visit):
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

    return cost, previous


def extract_all_paths(previous_nodes, start_node, target_node):
    # Stack to keep track of current path exploration
    stack = [(target_node, [target_node])]  # (current_node, current_path)
    all_paths = []

    while stack:
        current_node, path = stack.pop()

        # If the current node is the start node, we've found a complete path
        if current_node == start_node:
            all_paths.append(path[::-1])  # Reverse to get the path from start to target
            continue

        # Explore previous nodes for the current node
        if current_node in previous_nodes:
            for prev_node in previous_nodes[current_node]:
                stack.append((prev_node, path + [prev_node]))

    return all_paths


def convert_coords_to_dirpad(path):
    n = len(path)
    directions = []
    for i in range(0, n-1):
        y = path[i]
        x = path[i+1]
        delta_pos = (x[0] - y[0], x[1] - y[1])
        for dir, move in helper.STEP2POS.items():
            if helper.list_compare(delta_pos, move):
                arrow = helper.STEP2ARROW[dir]
                directions.append(arrow)
                break
    return directions


# Get start/end position
def solve(area, start_str, end_str, bound_x, bound_y):
    start_position = helper.find_position(area, start_str)
    end_position = helper.find_position(area, end_str)
    initialized_components = initialize_dijkstra(start_position, area, bound_x, bound_y)
    cost, previous = run_dijkstra(initialized_components)

    shortest_paths = extract_all_paths(previous, start_position, end_position)
    shortest_paths = [convert_coords_to_dirpad(x) for x in shortest_paths]
    return shortest_paths


def get_shortest_sequence(current_number):
    collection = {}

    for i in range(len(current_number) - 1):
        collection.setdefault(i, [])
        start_numpad = current_number[i]
        end_numpad = current_number[i + 1]
        dirpad_1_shortest_paths = solve(NUMPAD, start_numpad, end_numpad, NUMPAD_N_x, NUMPAD_N_y)
        print('(i) Dirpad 1 ', dirpad_1_shortest_paths)
        for jj, dirpad_1_shortest_path in enumerate(dirpad_1_shortest_paths):
            # We start navigating from 'A' and we need to end in 'A' to press the button
            dirpad_1_shortest_path = ['A'] + dirpad_1_shortest_path + ['A']
            print(f'(jj) Option: {jj}/{len(dirpad_1_shortest_paths) - 1} ', dirpad_1_shortest_path)
            n_dirpad_1 = len(dirpad_1_shortest_path)
            collection.setdefault((i, jj), [])
            for j in range(n_dirpad_1 - 1):
                start_dirpad_1 = dirpad_1_shortest_path[j]
                end_dirpad_1 = dirpad_1_shortest_path[j + 1]
                dirpad_2_shortest_paths = solve(DIRPAD, start_dirpad_1, end_dirpad_1, DIRPAD_N_x, DIRPAD_N_y)
                print(f'\t (j) Dirpad 2: {j}/{n_dirpad_1 - 2} ', dirpad_2_shortest_paths)
                collection.setdefault((i, jj, j), [])
                for kk, dirpad_2_shortest_path in enumerate(dirpad_2_shortest_paths):
                    # We start navigating from 'A' and we need to end in 'A' to press the button
                    dirpad_2_shortest_path = ['A'] + dirpad_2_shortest_path + ['A']
                    print(f'\t\t (kk) Option: {kk}/{len(dirpad_2_shortest_paths) - 1} ', dirpad_2_shortest_path)
                    collection.setdefault((i, jj, j, kk), [])
                    n_dirpad_2 = len(dirpad_2_shortest_path)
                    for k in range(n_dirpad_2 - 1):
                        start_dirpad_2 = dirpad_2_shortest_path[k]
                        end_dirpad_2 = dirpad_2_shortest_path[k + 1]
                        dirpad_3_shortest_paths = solve(DIRPAD, start_dirpad_2, end_dirpad_2, DIRPAD_N_x, DIRPAD_N_y)
                        print(f'\t\t\t Dirpad 3 ', dirpad_3_shortest_paths)
                        temp_3 = []
                        for ll, dirpad_3_shortest_path in enumerate(dirpad_3_shortest_paths):
                            dirpad_3_shortest_path = dirpad_3_shortest_path + ['A']
                            temp_3.append(''.join(dirpad_3_shortest_path))

                        collection[(i, jj, j, kk)].append(temp_3)

                    # Voor een 'j' zijn er meerdere mogelijkheden (kk)
                    # Hier voeg ik ze allemaal samen zodat ze gecombineerd kunnen worden met de volgende j
                    derp = list(itertools.product(*collection[(i, jj, j, kk)]))
                    derp = [''.join(x) for x in derp]
                    collection[(i, jj, j)].extend(derp)

                # Hier voeg ik alle onderdelen van 'zin' jj samen (bestaande uit 'j's)
                collection[(i, jj)].append(collection[(i, jj, j)])

            derp2 = list(itertools.product(*collection[(i, jj)]))
            derp2 = [''.join(x) for x in derp2]
            collection[i].extend(derp2)

    N = len(current_number) - 1
    s = ""
    for word_part in range(N):
        s += sorted(collection[word_part], key=len)[0]

    return s


DAY = "21"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

NUMPAD = ["789", "456", "123", "#0A"]
NUMPAD = [list(x) for x in NUMPAD]
NUMPAD_N_x = len(NUMPAD)
NUMPAD_N_y = len(NUMPAD[0])

DIRPAD = ["#^A", "<v>"]
DIRPAD = [list(x) for x in DIRPAD]
DIRPAD_N_x = len(DIRPAD)
DIRPAD_N_y = len(DIRPAD[0])

MAX_DIST = 1e10

"""
So...
my idea is that...
"""

s = 0
for iiii in ['029A']:
    current_number = "A" + iiii
    number = int(re.findall("([0-9]+)", current_number)[0])
    shortest_sequence = get_shortest_sequence(current_number)
    # print(number, len(shortest_sequence))
    s += number * len(shortest_sequence)

print(s)

"""
Okay... again!
"""


def get_sequence_recursive(start, end, depth):
    if (start, end, depth) in MEMORY:
        return MEMORY[(start, end, depth)]

    solutions = solve(DIRPAD, start, end, DIRPAD_N_x, DIRPAD_N_y)
    min_solution = math.inf
    for jj, solution in enumerate(solutions):
        # We always start and end with 'A'. Otherwise, we would never press the end result.
        solution = ['A'] + solution + ['A']
        length_solution = len(solution)
        if depth == N_MAX_DEPTH:
            # Remove one count, so that we 'remove' the first 'A'
            n_solution = length_solution - 1
        else:
            n_solution = 0
            for j in range(length_solution - 1):
                start_next = solution[j]
                end_next = solution[j + 1]
                # We should add the shortest sequences together
                n_solution += get_sequence_recursive(start_next, end_next, depth+1)
        if n_solution < min_solution:
            min_solution = n_solution

    MEMORY.setdefault((start, end, depth), min_solution)
    return min_solution

# When we solve the shortest path on the number
# We plug that in here.
# This always starts with A then goes to a number and we press A again

MEMORY = {}
N_MAX_DEPTH = 24
import math

def newfun(current_number):
    collection = {}
    shortest_number = 0
    for i in range(len(current_number) - 1):
        collection.setdefault(i, [])
        start_numpad = current_number[i]
        end_numpad = current_number[i + 1]
        shortest_paths = solve(NUMPAD, start_numpad, end_numpad, NUMPAD_N_x, NUMPAD_N_y)
        shortest_dirpad = math.inf
        for shortest_path in shortest_paths:
            shortest_path = ['A'] + shortest_path + ['A']
            temp = 0
            for j in range(len(shortest_path)- 1):
                start_dirpad = shortest_path[j]
                end_dirpad = shortest_path[j + 1]
                result = get_sequence_recursive(start_dirpad, end_dirpad, depth=0)
                temp += result
            if temp < shortest_dirpad:
                shortest_dirpad = temp
        shortest_number += shortest_dirpad

    return shortest_number

newfun('A029A')

s = 0
for iiii in puzzle_input:
    current_number = "A" + iiii
    number = int(re.findall("([0-9]+)", current_number)[0])
    shortest_sequence = newfun(current_number)
    # print(number, len(shortest_sequence))
    s += number * shortest_sequence

# too low
print(s)