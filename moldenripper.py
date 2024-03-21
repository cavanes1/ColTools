# Required input file:    molden.freq
# Generated output files: VIBS/*.xyz
conv = 0.529177211 # conversion factor

# module import
import numpy as np
import os

# read Molden frequency output file
f = open("molden.freq", "r")
lines = f.readlines()
f.close()

# extract data
geomline = 0
geomend = 0
viblines = []
for i in range(len(lines)):
    if "FR-COORD" in lines[i]:
        geomline = i
    if "FR-NORM-COORD" in lines[i]:
        geomend = i
    elif "vibration" in lines[i]:
        viblines.append(i)
natoms = geomend - geomline - 1

# extract geometry
geom = []
for i in range(geomline + 1, geomend):
    geom.append(lines[i].split())

# extract vibrations
vibnums = []
vibs = []
for i in viblines:
    vibnums.append(lines[i].split()[1])
    vib = []
    for j in range(i + 1, i + natoms + 1):
        vib.append(lines[j].split())
    vibs.append(vib)

# print
os.system("mkdir VIBS")
for i in range(len(viblines)):
    f = open("VIBS/" + str(vibnums[i]) + ".xyz", "w")
    f.write(str(natoms) + "\n\n")
    for atom in range(natoms):
        f.write(" " + format(geom[atom][0],"3s"))
        for j in range(3):
            f.write(format(float(geom[atom][j + 1])*conv,"13.6f"))
        for j in range(3):
            f.write(format(float(vibs[i][atom][j])*conv,"13.6f"))
        f.write("\n")
    f.close()
