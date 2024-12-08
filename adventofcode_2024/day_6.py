import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR
import copy


def find_position(A, direction='^'):
    for i, line in enumerate(A):
        if direction in line:
            j = line.index(direction)
            return i, j

def find_next_position(x, direction):
    if direction in ['^', '<']:
        step = 1   # +1 want 0, #, 2, ..., ^, ..., 7, #, end
        end = 0
    else:  # ['v', '>']
        step = -1   # -1 want 0, 1, 2, ..., v, ..., 7, #, end
        end = len(x)
    if '#' in x:
        return x.index('#') - step
    else:
        return end - step

def look_ahead(A, direction, position=None):
    if position is None:
        ix, iy = find_position(A, direction)
    else:
        ix, iy = position
    if direction in ['^', 'v']:
        path = helper.get_column(A, iy)
        if direction == '^':
            path = path[:ix][::-1]
        else:  # direction == 'v'
            path = path[ix+1:]
    else: # ['>', '<']:
        path = A[ix]
        if direction == '>':
            path = path[iy+1:]
        else:
            path = path[:iy][::-1]
    return path

def turn(x):
    turn_order = ['^', '>', 'v', '<']
    i = turn_order.index(x) + 1
    return turn_order[i % len(turn_order)]



def walk_the_walk(current_puzzle, start_direction="^", display=False, stop_at_start=False):
    inside = True
    current_direction = start_direction
    positions = {}
    while inside:
        # Get the position
        ix, iy = find_position(current_puzzle, direction=current_direction)
        positions.setdefault((ix,iy), [])
        positions[(ix, iy)].append(current_direction)
        # Look ahead
        path_ahead = look_ahead(current_puzzle, direction=current_direction)

        # We are going towards this position
        if '#' in path_ahead:
            new_position = path_ahead.index('#')
        else:
            new_position = len(path_ahead)
            inside = False
        # Store intermediate steps
        current_steps = []
        if current_direction == '^':
            current_steps = [(ix - ii, iy) for ii in range(1, new_position+1)]
        elif current_direction == 'v':
            current_steps = [(ix + ii, iy) for ii in range(1, new_position+1)]
        elif current_direction == '>':
            current_steps = [(ix, iy + ii) for ii in range(1, new_position+1)]
        elif current_direction == '<':
            current_steps = [(ix, iy - ii) for ii in range(1, new_position+1)]

        for coord in current_steps:
            if stop_at_start:
                res = positions.get(coord, None)
                if res is not None:
                    if current_direction in res:
                        print("Repeated position ", tuple(coord), current_direction)
                        return positions, 1

            positions.setdefault(coord, [])
            positions[coord].append(current_direction)

        if current_steps:
            final_position = current_steps[-1]
        else:
            final_position = (ix, iy)
        # THis is to display what we are doing
        if display:
            display_puzzle = copy.deepcopy(current_puzzle)
            display_puzzle[ix][iy] = "2"
            print('Current position', ix, iy, current_puzzle[ix][iy])
            print('Path ahead', path_ahead)
            for x in current_steps:
                display_puzzle[x[0]][x[1]] = "0"

            print('New position', final_position)
            display_puzzle[final_position[0]][final_position[1]] = "1"
            helper.print_binary([''.join(x) for x in display_puzzle])

        # update position
        current_puzzle[ix][iy] = '.'
        new_direction = turn(current_direction)
        current_puzzle[final_position[0]][final_position[1]] = new_direction
        current_direction = new_direction


    return positions, -1


DAY = "06"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = puzzle_input
chosen_puzzle = [list(x) for x in chosen_puzzle]

"""
Part 1
"""
part_1_puzzle = copy.deepcopy(chosen_puzzle)
positions, exit_code = walk_the_walk(part_1_puzzle)
print(len(positions))

"""
Part 2
"""

current_blokades = []
for ix, line in enumerate(chosen_puzzle):
    for iy, tile in enumerate(line):
        if tile == "#":
            current_blokades.append((ix, iy))

blokade_positions = []
for position, directions in positions.items():
    possible_position = None
    ix, iy = position
    for direction in directions:
        if direction == '^':
            # Look to the right side
            right_side =look_ahead(chosen_puzzle, direction=">", position=position)
            if '#' in right_side:
                # SO in front of us is then a possible position
                possible_position = [ix - 1, iy]
        elif direction == '>':
            right_side =look_ahead(chosen_puzzle, direction="v", position=position)
            if '#' in right_side:
                possible_position = [ix, iy + 1]
        elif direction == 'v':
            right_side =look_ahead(chosen_puzzle, direction="<", position=position)
            if '#' in right_side:
                possible_position = [ix + 1, iy]
        elif direction == '<':
            right_side =look_ahead(chosen_puzzle, direction="^", position=position)
            if '#' in right_side:
                possible_position = [ix - 1, iy]

        if possible_position:
            inside_x = 0 <= possible_position[0] < len(chosen_puzzle)
            inside_y = 0 <= possible_position[1] < len(chosen_puzzle)
            new_blokade = tuple(possible_position) not in current_blokades
            if inside_x and inside_y and new_blokade:
                blokade_positions.append(possible_position)


# Get unique blokades
unique_blokade_positions = set([tuple(x) for x in blokade_positions])

display_puzzle = copy.deepcopy(chosen_puzzle)
for position in blokade_positions:
    display_puzzle[position[0]][ position[1]] = "1"

helper.print_binary(display_puzzle)

"""
Now lets walk....
"""

temp = [x for x in positions.keys() if x != find_position(chosen_puzzle)]

count = 0
for extra_blokade in temp:
    extra_blokade_puzzle = copy.deepcopy(chosen_puzzle)
    extra_blokade_puzzle[extra_blokade[0]][extra_blokade[1]] = "#"
    positions, exit_code = walk_the_walk(extra_blokade_puzzle, stop_at_start=True, display=False)
    if exit_code == 1:
        count += 1
        print(extra_blokade, count)

# (6,3)
# (7,6)
# (7,7)
# (8,1)
# (8,3)
#