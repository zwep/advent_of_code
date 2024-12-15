import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "14"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)


def parse_puzzle(puzzle):
    positions = []
    velocity = []
    for iline in puzzle:
        position, speed = iline.split(" ")
        x, y = re.findall("([0-9]+)", position)
        vx, vy =  re.findall("(-|)([0-9]+)", speed)
        x = int(x)
        y = int(y)
        vx = int(''.join(vx))
        vy = int(''.join(vy))
        positions.append((x,y))
        velocity.append((vx, vy))
    return positions, velocity


chosen_puzzle = puzzle_input
positions, velocity = parse_puzzle(chosen_puzzle)


max_wide = 101
max_tall = 103
# Tets case
# max_wide = 11  # Tiles wide...
# max_tall = 7  # Tiles tall...

T0 = 0
T1 = 10000

def get_new_position(p0, v0, T, max_L):
    return (p0 + v0 * T) % max_L

from PIL import Image

quadrant_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
for iT in range(T0, T1):
    print(f"{iT}", end='\r')
    final_position = {}
    test_position = np.zeros((max_tall, max_wide))
    for p, v in zip(positions, velocity):
        x1 = get_new_position(p[0], v[0], iT, max_wide)
        y1 = get_new_position(p[1], v[1], iT, max_tall)
        final_position.setdefault((x1, y1), 0)
        final_position[(x1, y1)] += 1
        test_position[y1, x1] += 1
        if x1 < max_wide//2:
            if y1 < max_tall//2:
                quadrant_count['A'] += 1
            elif y1 > max_tall//2:
                quadrant_count['B'] += 1
        elif x1 > max_wide//2:
            if y1 < max_tall//2:
                quadrant_count['C'] += 1
            elif y1 > max_tall//2:
                quadrant_count['D'] += 1

    if any(test_position.sum(axis=1) > 0.2 * max_wide):
        image = Image.fromarray(test_position.astype(int).astype(np.uint8) * 255, mode='L')  # Specify 'RGBA' mode for 32 bits per pixel (8 bits per channel)
        image.save(os.path.expanduser(f"~/data/aoc_ax1_{iT}.png"))

    if any(test_position.sum(axis=0) > 0.2 * max_tall):
        image = Image.fromarray(test_position.astype(int).astype(np.uint8) * 255,
                                mode='L')  # Specify 'RGBA' mode for 32 bits per pixel (8 bits per channel)
        image.save(os.path.expanduser(f"~/data/aoc_ax0_{iT}.png"))

    # (test_position[:max_tall // 2, :] == test_position[max_tall // 2+1:, :][::-1]).sum()
    # if sum(test_position[max_tall//2, :]) == max_wide:
    #     print("WHAT", iT)
    # for k, v in final_position.items():
    #     print(k, v)
    #
    # helper.print_binary(test_position.astype(int).astype(str))
    # image = Image.fromarray(test_position.astype(int).astype(np.uint8) * 255, mode='L')  # Specify 'RGBA' mode for 32 bits per pixel (8 bits per channel)
    # image.save(os.path.expanduser(f"~/data/aoc_{iT}.png"))

# print(quadrant_count)
# import math
# math.prod(quadrant_count.values())