import os
from pathlib import Path

"""
Here we are going to define the paths.. there wont be much
"""

YEAR = "2024"
DDATA = '~/Documents/data/aoc'
DDATA = Path(DDATA).expanduser()

DCODE = '~/PycharmProjects/advent_of_code'
DCODE = Path(DCODE).expanduser()

# Set this variabel to determine from which day on we will generate the default py files
STARTING_DAY = 1

# Create data directory for the year
DDATA_YEAR = DDATA / YEAR

# Create code directory for the year
aoc_year = 'adventofcode_' + str(YEAR)
DCODE_YEAR = DCODE / aoc_year

DDEFAULT_DAY = DCODE / 'advent_of_code_helper/default_day.py'
DDEFAULT_DAY = Path(DDEFAULT_DAY)