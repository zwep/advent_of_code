from shutil import chown

import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR

DAY = "15"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')
DDATA_DAY_TEST_2 = os.path.join(DDATA_YEAR, DAY + '_test_2.txt')
DDATA_DAY_TEST_3 = os.path.join(DDATA_YEAR, DAY + '_test_3.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)
test_puzzle_input_2 = helper.read_lines_strip(DDATA_DAY_TEST_2)
test_puzzle_input_3 = helper.read_lines_strip(DDATA_DAY_TEST_3)


def parse_puzzle(puzzle):
    split_index = puzzle.index('')
    area = [list(x) for x in puzzle[:split_index]]
    moves = puzzle[split_index+1:]
    moves = list(''.join(moves))
    return area, moves


def substitute_puzzle(puzzle, new_str, direction, position):
    ix, iy = position
    if direction in ['^', 'v']:
        local_counter = 0
        for i, i_line in enumerate(puzzle):
            if (direction == '^') and (i < ix) and (local_counter < len(new_str)):
                i_line[iy] = new_str[len(new_str)-local_counter-1]
                local_counter += 1
            if (direction == 'v') and (i > ix) and (local_counter < len(new_str)):
                i_line[iy] = new_str[local_counter]
                local_counter += 1
    else:  # ['>', '<']:
        if direction == '>':
            puzzle[ix][iy + 1:iy +1 + len(new_str)] = new_str
        else:
            puzzle[ix][iy-len(new_str):iy] = new_str[::-1]
    return puzzle


def get_wide_area(area):
    # Increase the size...
    new_area = []
    for line in area:
        new_line = []
        for tile in line:
            if tile == 'O':
                new_tile = ['[', ']']
            elif tile == "@":
                new_tile = ["@", "."]
            else:
                new_tile = [tile] * 2
            new_line.extend(new_tile)

        new_area.append(new_line)
    return new_area


chosen_puzzle = test_puzzle_input
area, moves = parse_puzzle(chosen_puzzle)

#
#
# print("Initial state")
# for move in moves:
#     helper.print_binary(area)
#     print("Move ", move)
#     current_position = helper.find_position(area, "@")
#     ahead = helper.look_ahead(area, direction=move, position=current_position)
#     wall_piece = ahead.index("#")
#     if '.' in ahead:
#         empty_piece = ahead.index(".")
#     else:
#         continue
#
#     if empty_piece < wall_piece:
#         # There is room!
#         new_ahead = ["@"] + list(ahead[:empty_piece]) + list(ahead[empty_piece+1:])
#         # Now substitute that piece into the puzzle again and start over
#         substitute_puzzle(area, new_str=new_ahead, direction=move, position=current_position)
#         area[current_position[0]][current_position[1]] = "."
#     else:
#         # No..
#         continue
#
# box_positions = helper.find_positions(area, marker='O')
# sum([x[0] * 100 + x[1] for x in box_positions])

"""
Part 2
"""

chosen_puzzle = test_puzzle_input
area, moves = parse_puzzle(chosen_puzzle)
wide_area = get_wide_area(area)

print("Initial state")
while len(moves):
    move = moves.pop(0)
    helper.print_binary(wide_area)
    print("Move ", move)
    current_position = helper.find_position(wide_area, "@")
    to_check_positions = [current_position]
    ok_or_not_okay = []
    positions_and_substitutions = {}
    while len(to_check_positions):
        to_check_position = to_check_positions.pop()
        print(to_check_position)
        ahead = helper.look_ahead(wide_area, direction=move, position=to_check_position)
        wall_piece = ahead.index("#")
        if '.' in ahead:
            empty_piece = ahead.index(".")
        else:
            ok_or_not_okay.append(False)
            continue

        if empty_piece < wall_piece:
            # There is atleast some room!
            push_part = list(ahead[:empty_piece])
            # Only do this when we go up or down?
            if move in ['v', '^']:
                # Check if there are more positions to check
                for i, push in enumerate(push_part):
                    if push == '[':
                        if move == "^":
                            check_position = (to_check_position[0]-i, to_check_position[1] + 1)
                        else:  # "v"
                            check_position = (to_check_position[0]+i, to_check_position[1] + 1)
                    elif push == ']':
                        if move == "^":
                            check_position = (to_check_position[0]-i, to_check_position[1] - 1)
                        else:  # "v"
                            check_position = (to_check_position[0]+i, to_check_position[1] - 1)
                    else:
                        continue

                    # Only add it if we have not planned something already
                    # # And... don't add positions above or below us
                    if check_position not in positions_and_substitutions:
                        to_check_positions.append(check_position)

            new_tile = "."
            if current_position == to_check_position:
                new_tile = "@"

            new_ahead = [new_tile] + push_part # + list(ahead[empty_piece+1:])
            ok_or_not_okay.append(True)
            positions_and_substitutions[to_check_position] = new_ahead
        else:
            # No..
            ok_or_not_okay.append(False)
            continue

    # check the positions and substitutions..?
    # Only apply those that are the lowest when going upwards
    # Or the lowest when going down...
    if all(ok_or_not_okay):
        allowed_positions = list(positions_and_substitutions.keys())
        if move in ['v', '^']:
            filtered_allowed_positions = []
            for position in allowed_positions:
                if wide_area[position[0]][position[1]] == '.':
                    filtered_allowed_positions.append(position)
            # This was not good enough
            # column_levels = set([x[1] for x in allowed_positions])
            # for column_level in column_levels:
            #     temp = [x for x in allowed_positions if x[1] == column_level]
            #     if move == 'v':
            #         single_position = min(temp, key = lambda x: x[0])
            #     else:  # "^"
            #         single_position = max(temp, key=lambda x: x[0])
            #     filtered_allowed_positions.append(single_position)
            allowed_positions = filtered_allowed_positions
        else:
            pass
        for position in allowed_positions:
            substitution = positions_and_substitutions[position]
            substitute_puzzle(wide_area, new_str=substitution, direction=move, position=position)
            if position == current_position:
                wide_area[current_position[0]][current_position[1]] = "."

left_boxes = helper.find_positions(wide_area, '[')
print(sum([x[0] * 100 + x[1] for x in left_boxes]))

# 1469407 too low
# 1471174 too low