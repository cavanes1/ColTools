choice = 1 # vibration to consider

# module import
import numpy as np
import os

# extract data
f = open("MOLDEN/molden.freq", "r")
lines = f.readlines()
f.close()
# number of atoms
atom_count = 6

# old geometry
# line before first atom
firstline = 0
# line after last atom
lastline = 0
# lines before vibrations
viblines = []
count = 0 # current line
# go through all lines in the file
for line in lines:
    # geometry
    if "[FR-COORD]" in line:
        # this is the top
        firstline = count + 1
        # this is the bottom
        lastline = firstline + atom_count - 1
    # vibration matrices
    if "vibration" in line:
        # top
        viblines.append(count + 1)
    # we're done with this line, onto the next
    count += 1

# extract coordinates
oldgeom = []
for i in range(firstline, lastline + 1):
    temporary_list = lines[i].split()[1:4]
    temporary_list = [float(i) for i in temporary_list]
    oldgeom.append(temporary_list)
oldgeom = np.array(oldgeom)
print("Old geometry")
print(oldgeom)

# extract vibrations
vibs = []
for i in range(len(viblines)):
    tempvib = []
    for i in range(viblines[i], viblines[i] + atom_count):
        temporary_list = lines[i].split()[0:3]
        temporary_list = [float(i) for i in temporary_list]
        tempvib.append(temporary_list)
    vibs.append(tempvib)
vibs = np.array(vibs)
print("Raw vibration matrix")
print(vibs[choice-1])

# normalize matrices
norm_vibs = []
for i in range(len(vibs)):
    norm = np.linalg.norm(vibs[i]) # axis = 0
    norm_vibs.append(vibs[i]/norm)
norm_vibs = np.array(norm_vibs)
print("Normalized vibration matrix")
print(norm_vibs[choice-1])

# make space for updated geom file
os.system("mv geom oldgeom")

# generate new matrix
new_geom = []
for i in range(len(norm_vibs)):
    matrix = oldgeom + (norm_vibs[i]/5)
    new_geom.append(matrix)
new_geom = np.array(new_geom)
print("New geometry")
print(new_geom[choice-1])

# overwrite geom
g = open("geom", "w")
count = 0

def writecartesian(arr):
    xstr = format(arr[0], "14.8f")
    ystr = format(arr[1], "14.8f")
    zstr = format(arr[2], "14.8f")
    return xstr + ystr + zstr

# write to file
g.write(" S    16.0" + writecartesian(new_geom[choice - 1][0]) + "   31.97207117\n")
g.write(" C     6.0" + writecartesian(new_geom[choice - 1][1]) + "   12.00000000\n")
g.write(" H     1.0" + writecartesian(new_geom[choice - 1][2]) + "    1.00782504\n")
g.write(" H     1.0" + writecartesian(new_geom[choice - 1][3]) + "    1.00782504\n")
g.write(" H     1.0" + writecartesian(new_geom[choice - 1][4]) + "    1.00782504\n")
g.write(" H     1.0" + writecartesian(new_geom[choice - 1][5]) + "    1.00782504\n")
g.close()