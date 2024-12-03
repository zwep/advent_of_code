from advent_of_code_helper.configuration import DDATA_YEAR, DCODE_YEAR, DDEFAULT_DAY, STARTING_DAY
import re
import os
import shutil
from pathlib import Path


def write_new_default_day(day: int):
    with open(DDEFAULT_DAY, 'r') as f:
        default_day_txt = f.read()

    default_day_txt = re.sub(":day_value:", str(day).zfill(2), default_day_txt)

    with open(file_path, 'w') as f:
        f.write(default_day_txt)

    print(f'\t Written day {ii} to {file_path}')

"""
Create the necessary directories
"""

os.makedirs(DDATA_YEAR, exist_ok=True)
os.makedirs(DCODE_YEAR, exist_ok=True)

"""
Create all the days with a default structure
"""

num_days = 25
for ii in range(STARTING_DAY, num_days + 1):
    file_path = Path(DCODE_YEAR) / f'day_{ii}.py'
    # Now copy the default...
    if file_path.is_file():
        print(f"Day {ii} already exists")
        # Default is no
        result = input('Overwrite file? y / [n]') or "n"
        if result == 'y':
            write_new_default_day(ii)
        else:
            print(f'\t Skipped day {ii}')
        print()
    else:
       write_new_default_day(ii)
