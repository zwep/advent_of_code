import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR
import itertools

DAY = "23"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = puzzle_input

connection_clusters = []
# while len(chosen_puzzle):
for connection in chosen_puzzle:
    cpu1, cpu2 = connection.split("-")
    cpu1_connections = set([re.sub("-", "", re.sub(cpu1, "", x)) for i, x in enumerate(chosen_puzzle) if (cpu1 in x) and (cpu2 not in x)])
    cpu2_connections = set([re.sub("-", "", re.sub(cpu2, "", x)) for i, x in enumerate(chosen_puzzle) if (cpu2 in x) and (cpu1 not in x)])
    cpu3_connections = list(cpu2_connections.intersection(cpu1_connections))
    for cpu3 in cpu3_connections:
        trio = tuple(sorted([cpu1, cpu2, cpu3]))
        if 't' not in [x[0] for x in trio]:
            continue

        if trio not in connection_clusters:
            connection_clusters.append(trio)

# Get uni
len(connection_clusters)

"""
Part 2
"""

puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

chosen_puzzle = puzzle_input
all_cpus = [x.split("-") for x in chosen_puzzle]
all_cpus = sorted(list(set(itertools.chain(*all_cpus))))
import numpy as np
n = len(all_cpus)
A = np.zeros((n, n))

for connection in chosen_puzzle:
    cpu1, cpu2 = connection.split("-")
    ind1 = all_cpus.index(cpu1)
    ind2 = all_cpus.index(cpu2)
    A[ind1][ind2] += 1

A = (A + A.T)
# Visualize stuff
helper.print_binary(A.astype(int).astype(str))

result = {}
for i in range(n):
    ind_A = np.where(A[i] == 1)[0]

    z = []
    for j in ind_A:
        z.append(A[j][ind_A])

    result[i] = {'A': np.array(z), 'ind': ind_A}

derp = []
for k, v in result.items():
    temp = v['A']
    np.fill_diagonal(temp, 1)
    # temp[np.tril_indices(len(temp))] = 0
    # print(all_cpus[k], "\n", v['A'], )
    for i in range(len(v['ind'])):
        if i == 0:
            if np.all(temp == 1):
                # print("We have a full id matrix ", v['ind'])
                pass
        else:
            if np.all(temp[:-i, :-i] == 1):
                # print("We have a full id matrix ", v['ind'], i)
                derp.append((k, i))
                break

derp = sorted(derp, key=lambda x: x[1])
name = derp[0][0]
print(result[name]['A'])
for ii in result[name]['ind']:
    print(ii, result[ii]['ind'])
    print(result[ii]['A'])


','.join(sorted([all_cpus[x] for x in result[357]['ind'][:-1].tolist() + [357]]))

# ao,es,fe,if,in,io,ky,qq,rd,rn,vc,vl not the answer....