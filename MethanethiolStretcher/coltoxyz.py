# module import
import numpy as np
import os

# extract data
f = open("geom.min", "r")
lines = f.readlines()
f.close()
# number of atoms
atom_count = 6

# extract coordinates
oldgeom = []
for i in lines:
    temporary_list = i.split()[2:5]
    temporary_list = [float(i) for i in temporary_list]
    oldgeom.append(temporary_list)
oldgeom = np.array(oldgeom)
print("Old geometry")
print(oldgeom)

# overwrite geom
g = open("geom.xyz", "w")
count = 0

def writecartesian(arr):
    xstr = format(arr[0], "13.6f")
    ystr = format(arr[1], "13.6f")
    zstr = format(arr[2], "13.6f")
    return xstr + ystr + zstr

# write to file
g.write("6\n\n")
g.write(" S  " + writecartesian(oldgeom[0]) + "\n")
g.write(" C  " + writecartesian(oldgeom[1]) + "\n")
g.write(" H  " + writecartesian(oldgeom[2]) + "\n")
g.write(" H  " + writecartesian(oldgeom[3]) + "\n")
g.write(" H  " + writecartesian(oldgeom[4]) + "\n")
g.write(" H  " + writecartesian(oldgeom[5]) + "\n")
g.close()
