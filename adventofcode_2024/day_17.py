import copy

import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "17"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')
DDATA_DAY_TEST_2 = os.path.join(DDATA_YEAR, DAY + '_test_2.txt')


# Run get data...
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)


def parse_puzzle(puzzle):
    split_index = puzzle.index('')
    registers_list = puzzle[:split_index]
    program = puzzle[split_index+1:]
    program = helper.int_str2list(''.join(program).split(":")[-1], sep=',')
    registers = {}
    for register in registers_list:
        register_name, register_value = register.split(":")
        register_name = register_name[-1]
        register_value = int(re.findall("([0-9]+)", register_value)[0])
        registers[register_name] = register_value
    return registers, program


def parse_combo_operand(operand):
    """
    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of REGISTER A.
    Combo operand 5 represents the value of REGISTER B.
    Combo operand 6 represents the value of REGISTER C.
    Combo operand 7 is reserved and will not appear in valid programs.
    """
    if operand in [0, 1, 2, 3]:
        combo_operand = operand
    elif operand == 4:
        combo_operand = REGISTER['A']
    elif operand == 5:
        combo_operand = REGISTER['B']
    elif operand == 6:
        combo_operand = REGISTER['C']
    elif operand == 7:
        combo_operand = None
        print("Invalid operand")
    else:
        combo_operand = None
        print("You shouldnt be here")
    return combo_operand


def parse_opcode(opcode, operand):
    output = None
    pointer = None
    # The adv instruction (opcode 0) performs division.
    # The numerator is the value in the A REGISTER.
    # The denominator is found by raising 2 to the power of the instruction's combo operand.
    # The result of the division operation is truncated to an integer and then written to the A REGISTER.
    if opcode == 0:
        REGISTER['A'] = int(REGISTER['A'] / (2 ** parse_combo_operand(operand)))
    # The bxl instruction (opcode 1) calculates the bitwise XOR of REGISTER B and
    # the instruction's literal operand, then stores the result in REGISTER B.
    elif opcode == 1:
        REGISTER['B'] = REGISTER['B'] ^ operand
    # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
    # (thereby keeping only its lowest 3 bits), then writes that value to the B REGISTER.
    elif opcode == 2:
        # Is it always a combo operand?
        REGISTER['B'] = parse_combo_operand(operand) % 8
    # The jnz instruction (opcode 3) does nothing if the A REGISTER is 0.
    # However, if the A REGISTER is not zero, it jumps by setting the instruction pointer to the value of its
    # literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
    elif opcode == 3:
        if REGISTER['A'] == 0:
            pass
        else:
            pointer = operand
    # The bxc instruction (opcode 4) calculates the bitwise XOR of REGISTER B and REGISTER C,
    # then stores the result in REGISTER B. (For legacy reasons, this instruction reads an operand but ignores it.)
    elif opcode == 4:
        REGISTER['B'] = REGISTER['B'] ^ REGISTER['C']
    # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
    # (If a program outputs multiple values, they are separated by commas.)
    elif opcode == 5:
        # Is it always a combo operand?
        output = parse_combo_operand(operand) % 8
    # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B REGISTER.
    # (The numerator is still read from the A REGISTER.)
    elif opcode == 6:
        REGISTER['B'] = int(REGISTER['A'] / (2 ** parse_combo_operand(operand)))
    # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C REGISTER.
    # (The numerator is still read from the A REGISTER.)
    elif opcode == 7:
        REGISTER['C'] = int(REGISTER['A'] / (2 ** parse_combo_operand(operand)))
    else:
        print("We shouldnt be here")
    return output, pointer

def list_compare(x, y):
    return all([ix == iy for ix, iy in zip(x,y )])

def run_program(program):
    pointer = 0
    stdout = []
    while True:
        # If the computer tries to read an opcode past the end of the program, it instead halts.
        if pointer >= (len(program) - 1):
            break

        # instructions are each identified by a 3-bit number (called the instruction's opcode).
        opcode = program[pointer]
        # Each instruction also reads the 3-bit number after it as an input; this is called its operand.
        operand = program[pointer + 1]

        # the instruction pointer identifies the position in the program from which the next opcode will be read;
        # it starts at 0, pointing at the first 3-bit number in the program.
        # Except for jump instructions, the instruction pointer increases by 2 after each instruction is processed
        # (to move past the instruction's opcode and its operand)
        # --> if == jump --> pointer + 22

        output, new_pointer = parse_opcode(opcode, operand)
        if new_pointer == None:
            pointer += 2
        else:
            pointer = new_pointer
        #
        if output is not None:
            stdout.append(output)
    return stdout



# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)
test_puzzle_input_2 = helper.read_lines_strip(DDATA_DAY_TEST_2)


chosen_puzzle = puzzle_input
REGISTER_BACKUP, program = parse_puzzle(chosen_puzzle)

for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] =i
    stdout = run_program(program)
    print(i, stdout)
# --> it is 4

for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = 4 * 8 + i
    stdout = run_program(program)
    print(i, stdout)

# --> it is 5 or 7

# is it 5? it is
# is it 7? no
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = (4 * 8 + 5) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# --> it is 3


# is it... 5?
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = ((4 * 8 + 5) * 8 + 3) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 2


# is it... 3?
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = (((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 3

# is it 0?
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = ((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 0 or 5


# is it 5?
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = (((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# if 0 then choose 5
# if 5 then choose 3


# we want 4 (choosing ... 5)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = ((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 1


# we want 5 (choosing 1)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = (((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 3


# we want 1 (choosing 3)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = ((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 3


# we want 5 (choosing 3)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = (((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + 3) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 2


# we want 7 (choosing 2)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = ((((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + 3) * 8 + 2) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 6


# we want 1 (choosing 6)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = (((((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + 3) * 8 + 2) * 8 + 6) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 7


# we want 1 (choosing 7)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = ((((((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + 3) * 8 + 2) * 8 + 6) * 8 + 7) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 2


# we want 4 (choosing 2)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = (((((((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + 3) * 8 + 2) * 8 + 6) * 8 + 7) * 8 + 2) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 0


# we want 2 (choosing 0 (X), 1(X), 2(X), 5(X) ,7)
for i in range(8):
    REGISTER = copy.deepcopy(REGISTER_BACKUP)
    REGISTER['A'] = ((((((((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + 3) * 8 + 2) * 8 + 6) * 8 + 7) * 8 + 2) * 8 + 7) * 8 + i
    stdout = run_program(program)
    print(i, stdout)
# choose 5

final_result = ((((((((((((((4 * 8 + 5) * 8 + 3) * 8 + 2) * 8 + 3) * 8 + 0) * 8 + 5) * 8 + 1) * 8 + 3) * 8 + 3) * 8 + 2) * 8 + 6) * 8 + 7) * 8 + 2) * 8 + 7) * 8 + 5


chosen_puzzle = puzzle_input
REGISTER_BACKUP, program = parse_puzzle(chosen_puzzle)
REGISTER = copy.deepcopy(REGISTER_BACKUP)
REGISTER['A'] = final_result
stdout = run_program(program)