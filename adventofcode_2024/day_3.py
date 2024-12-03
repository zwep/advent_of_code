import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def mul_prod(x:str):
    a, b = map(int, re.sub('mul\\(|\\)', '', mul).split(","))
    return a * b

DAY = "03"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

regex = re.compile("(mul\\([0-9]{1,3},[0-9]{1,3}\\))")

chosen_puzzle = puzzle_input
chosen_puzzle = ''.join(chosen_puzzle)
muls = regex.findall(chosen_puzzle)

prod = 0
for mul in muls:
    prod += mul_prod(mul)


"""
Part 2
"""


regex_do_dont = re.compile("(.*?)(mul\\([0-9]{1,3},[0-9]{1,3}\\))")
do_dont_muls = regex_do_dont.findall(chosen_puzzle)

doing = True
prod = 0
check_dont = "don't()"
check_do = "do()"

for scrap, mul in do_dont_muls:
    # Always start out clean
    index_dont = 9999999
    index_do = 9999999

    # Take the reverse because then we get the last one....
    rev_scrap = scrap[::-1]
    if check_dont in scrap:
        index_dont = rev_scrap.index(check_dont[::-1])

    if check_do in scrap:
        index_do = rev_scrap.index(check_do[::-1])

    if index_do > index_dont:
        doing = False
    elif index_do < index_dont:
        doing = True
    else:
        # They are equal... hence no scrap was there
        pass

    print(scrap, mul, doing)
    if doing:
        prod += mul_prod(mul)
