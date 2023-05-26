# module import
import numpy as np
import os

# read from polyhesls
f = open("LISTINGS/polyhesls.all", "r")
lines = f.readlines()
f.close()

# extract data from polyhesls
position = 0
iteration = 0
data = []
normlist = []
for line in lines:
    if "iteration" in line:
        iteration = int(line.split()[3])
        data.append(iteration)
    if "OLD NORM" in line:
        norm_string = line.split()[7]
        norm = float(norm_string)
        normlist.append(norm)

# print data
print("Number of iterations: " + str(len(data)))
print(data)
print("Number of norms: " + str(len(normlist)))
print(normlist)
