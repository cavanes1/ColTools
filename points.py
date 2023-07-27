nstates = 3

# import modules
import numpy as np

# open file
f = open("energy.all", "r")
Elines = f.readlines()
f.close()

# extract data
E_data = []
for line in Elines:
    line = line[:-1]
    print(line)
    E_data.append(line.split())

# Try to find which points are degenerate
# convert energies to wavenumbers
Eincm = []
for point in E_data:
    Eincm.append([])
    for state in point:
        EN = state
        ENcm = float(EN) * 219475
        Eincm[-1].append(ENcm)

# calculate energy differences
diffs = []
for point in Eincm:
    diff = []
    for i in range(len(point)-1):
        diff.append(point[i+1]-point[i])
    diffs.append(diff)

# write to file
f = open("points.garbage", "w")
f.write("POINT SPECIFIC OPTIONS\n")
f.write("JOB PT  I   J\n")
pointnum = 1
for point in diffs:
    diffnum = 1
    for difference in point:
        if difference < 350:
            f.write("EG" + format(pointnum, "6d") + format(diffnum, "5d") + format(diffnum, "5d") + "\n")
            f.write("EG" + format(pointnum, "6d") + format(diffnum, "5d") + format(diffnum + 1, "5d") + "\n")
            f.write("EG" + format(pointnum, "6d") + format(diffnum + 1, "5d") + format(diffnum + 1, "5d") + "\n")
        diffnum += 1
    pointnum += 1
f.close()

# remove duplicate lines
lines_seen = set() # holds lines already seen
outfile = open("points.in", "w")
for line in open("points.garbage", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
