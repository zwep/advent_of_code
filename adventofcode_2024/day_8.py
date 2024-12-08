import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR
import copy


def get_distance(p0, p1):
    delta_x, delta_y = get_delta(p0, p1)
    return (delta_x ** 2 + delta_y ** 2) ** 0.5


def get_delta(p0, p1):
    # (delta_x, delta_y)
    return p1[0] - p0[0], p1[1] - p0[1]


def validate_coordinate(p, upper_bound):
    if (0 <= p[0] < upper_bound) and (0 <= p[1] < upper_bound):
        return True

def get_unique_frequencies(radar_map):
    return list(set(re.sub("\\.", "", ''.join(radar_map))))

# Collect all the radars
def get_coordinates_radar(radar_map, frequency):
    frequency_nodes = []
    for ix, line in enumerate(radar_map):
        for iy, node in enumerate(line):
            if node == frequency:
                frequency_nodes.append((ix, iy))
    return frequency_nodes

# Now create all the pairs...
def get_radar_pairs(frequency_nodes):
    # We start by getting ALL the combinations
    # We could filter based on the distances and the input size
    n = len(frequency_nodes)
    # Sorts on the first key - the x-coordinate
    frequency_nodes = sorted(frequency_nodes, key=lambda x: (x[0], x[1]))
    radar_pairs = []
    for i in range(n):
        current_node = frequency_nodes[i]
        for j in range(i+1, n):
            pair = (current_node, frequency_nodes[j])
            # d = get_distance(*pair)
            # if d > ...:
            # else:
            radar_pairs.append(pair)
    return radar_pairs


def get_antinodes(pair, upper_bound):
    delta_x, delta_y = get_delta(*pair)
    p0, p1 = pair
    # Repeat this
    antinodes = []
    for ii in range(upper_bound * 4):
        p0_antinode = p0[0] - ii * delta_x, p0[1] - ii * delta_y
        p1_antinode = p1[0] + ii * delta_x, p1[1] + ii * delta_y
        antinodes.extend([p0_antinode, p1_antinode])
    return [x for x in antinodes if validate_coordinate(x, upper_bound)]


DAY = "08"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = puzzle_input
display_puzzle = copy.deepcopy(chosen_puzzle)
display_puzzle = [list(x) for x in display_puzzle]

n_max = len(chosen_puzzle)  # it is square
unique_frequencies = get_unique_frequencies(chosen_puzzle)
antinodes = {}
all_radars = []
for sel_frequency in unique_frequencies:
    coordinates_radar = get_coordinates_radar(chosen_puzzle, sel_frequency)
    all_radars.extend(coordinates_radar)
    radar_pairs = get_radar_pairs(coordinates_radar)
    antinodes.setdefault(sel_frequency, [])
    for pair in radar_pairs:
        antinodes[sel_frequency].extend(get_antinodes(pair, n_max))

for frequency, antinode in antinodes.items():
    for inode in antinode:
        display_puzzle[inode[0]][inode[1]] = "1"

helper.print_binary(display_puzzle)

#
all_antinodes = []
for k, v in antinodes.items():
    all_antinodes.extend(v)


len(set(all_antinodes))
# overlap = set(all_antinodes).intersection(set(all_radars))
# n = len(all_antinodes)
# # aha, er zijn dubbele...
# n - len(overlap)

x = list(range(10))

dict(zip(x, x))
for x,y in zip(x,x):
    print(x,y)


    x == 2 and x== 3

