import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "22"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)


def process_secret_number(x):
    # Step 1:
    x = (2 ** 6 * x ^ x) % 2 ** 24
    # Step 2:
    x = (int(x // 2 ** 5) ^ x) % 2 ** 24
    # Step 3:
    x = (2 ** 11 * x ^ x) % 2 ** 24
    return x


# Collect the first occurence of each pattern (length 4)
def get_pattern_power(sequences):
    n = len(sequences)
    prices, differences = zip(*sequences)
    pattern_power = {}
    for i in range(n - 4 + 1):
        new_pattern = differences[i:i+4]
        if new_pattern in pattern_power:
            continue
        else:
            # pattern_power.setdefault(new_pattern, prices[i+4-1])
            pattern_power[new_pattern] = prices[i + 4 - 1]
    return pattern_power


chosen_puzzle = puzzle_input
# chosen_puzzle = ['1', '2', '3', '2024']
N = 2000
result = {}
for y in chosen_puzzle:
    x = int(y)
    sequences = [(x % 10, None)]
    for _ in range(N):
        prev_x = x % 10
        x = process_secret_number(x)
        sequences.append((x % 10, (x % 10) - prev_x))
    result[y] = sequences

result_patterns = {}
all_patterns = set()
for starting_nr, sequences in result.items():
    result_patterns.setdefault(starting_nr, {})
    pattern_power = get_pattern_power(sequences[1:])
    result_patterns[starting_nr] = pattern_power
    all_patterns.update(list(pattern_power.keys()))

# Now choose which pattern can maximize the result over ALL the initial numbers
performance_pattern = {}
for pattern in all_patterns:
    # Calculate the gain of this one...
    s = 0
    for k, v in result_patterns.items():
        s += v.get(pattern, 0)

    performance_pattern[pattern] = s

max_performer = max(performance_pattern, key = performance_pattern.get)
print(max_performer, performance_pattern[max_performer])
#
# # 2052 -- too high: pattern (0, 0, -1, 1)
# # Is it all correct..?
# target_pattern = (0, 0, -1, 1)
#
# relevant_input = []
# for j in chosen_puzzle:
#     w = result_patterns[j].get(target_pattern)
#     if w is not None:
#         relevant_input.append(j)
#
# # Find one that has something
# # result_patterns[j].get(target_pattern)
#
# z = relevant_input[0]
# prices, differences = zip(*result[z])
# for i in range(len(differences)):
#     if helper.list_compare(differences[i:i+4], list(target_pattern)):
#         break
# else:
#     print("ehm")
#
# print(differences[i:i+4])
# print(prices[i-1:i+4])
# print(prices[i+4-1])