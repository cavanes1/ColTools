# module imports
import numpy as np
import os
import subprocess
import sys
print("\nall modules imported\n")

# extract energies
E1list = []
minElist = []
Difflist = []
iterlist = []
f = open('./LISTINGS/energy.all', "r")
lines = f.readlines()
for i in range(3, len(lines), 6):
    line = lines[i]
    E1list.append(float(line.split()[0]))
    minElist.append(float(line.split()[1]))
    Difflist.append(float(line.split()[2]))
    iterlist.append(int(lines[i-2].split()[3]))

# calculate energy differences
delE1 = []
delE2 = []
delDIFF = []
delITER = []
cf = 219474.63136
for i in range(1, len(iterlist)):
    delE1.append((E1list[i] - E1list[i - 1])*cf)
    delE2.append((minElist[i] - minElist[i - 1])*cf)
    delDIFF.append((Difflist[i] - Difflist[i - 1])*cf)
    delITER.append(iterlist[i])

# find minimum E2 value
miniter = 0
minen = 0
for directory in range(len(iterlist)):
    if minElist[directory] < minen:
        miniter = directory
        minen = minElist[directory]

print("The lowest energy is " + str(minen) + " at iteration " + str(iterlist[miniter]))

# print output
# Hartrees
'''
print("\nIter  deltaE1         deltaE2         Diff\n")
for i in range(len(delITER)):
    print("{e:3.0f}  {b:13.10f}   {c:13.10f}   {d:13.10f}".format(e = delITER[i], b = delE1[i], c = delE2[i], d = delDIFF[i]))
'''
# wavenumbers
print("\nIter   deltaE1    deltaE2     Diff\n")
for i in range(len(delITER)):
    print("{e:3.0f} {b:10.3f} {c:10.3f} {d:10.3f}".format(e = delITER[i], b = delE1[i], c = delE2[i], d = delDIFF[i]))
