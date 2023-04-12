# module imports
import numpy as np
import os
import subprocess
import sys
print("\nall modules imported\n")

# make list of CI searches
path = './'
directories = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
print("finished producing directory list\n")

searches = []
others = []
for directory in directories:
    if os.path.exists('./' + directory + '/LISTINGS/energy.all'):
        if "G" not in directory:
            searches.append(directory)
        else:
            others.append(directory)
    else:
        others.append(directory)
print("List of directories without energy.all")
print(others)
print("\nList of directories with energy.all")
print(searches)

# extract lowest energies
E1list = []
minElist = []
Difflist = []
iterlist = []
for directory in searches:
    f = open('./' + directory + '/LISTINGS/energy.all', "r")
    lines = f.readlines()
    minE = 0
    minline = 0
    for i in range(3, len(lines), 6):
        line = lines[i]
        E2 = float(line.split()[1])
        if E2 < minE:
            minE = E2
            minline = i
    E1list.append(float(lines[minline].split()[0]))
    minElist.append(float(lines[minline].split()[1]))
    Difflist.append(float(lines[minline].split()[2]))
    iterlist.append(int(lines[minline-2].split()[3]))


# print results
mindct = 0
minen = 0
for directory in range(len(searches)):
    if minElist[directory] < minen:
        mindct = directory
        minen = minElist[directory]

print("\nThe lowest energy is " + str(minen))
print("Source: " + searches[mindct] + "/LISTINGS/energy.all\n")

# generating sorted list
uE2 = np.array(minElist)
sortedMinE = np.argsort(uE2)
sDr = np.array(searches)[sortedMinE]
sE1 = np.array(E1list)[sortedMinE]
sE2 = uE2[sortedMinE]
SDf = np.array(Difflist)[sortedMinE]
sI = np.array(iterlist)[sortedMinE]

# print output
print("Directory  Iter E1                E2                Diff\n")
for i in range(len(sDr)):
    print("{a:<9}  {e:3.0f}  {b:10.10f}   {c:10.10f}   {d:10.10f}".format(a = sDr[i], e = sI[i], b = sE1[i], c = sE2[i], d = SDf[i]))
