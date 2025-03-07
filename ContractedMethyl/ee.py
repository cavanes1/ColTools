CI = True

# module imports
import numpy as np
import subprocess
import os

# generate list of all files
path = './'
flist = os.listdir(path)

# narrow down to output files
geomfiles = []
for file in flist:
    if ".out" in file and "slurm" not in file:
        geomfiles.append(file)

# output lists
MCenergies = []
CIenergies = []
MCiterations = []
CIiterations = []

prog = 1
# extract data
for outfile in geomfiles:
    print('Starting ' + str(prog) + ' of ' + str(len(geomfiles)) + ': ' + outfile)
    f = open(outfile, "r")
    lines = f.readlines()

    # MCSCF
    # Identify final iteration
    lastline = 0
    for line in lines:
        lastline += 1
        if "CONVERGENCE REACHED, FINAL GRADIENT:" in line:
            lastline -= 3
            break
    iterstring = lines[lastline][:6]
    # Energies
    CCE = [] # current conformation energies
    for line in lines:
        if "!MCSCF STATE " in line and " Energy" in line:
            CCE.append(float(line[38:54]))
    MCenergies.append(CCE)
    MCiterations.append(iterstring.replace(" ", ""))

    # CI
    if CI:
        # first line of text after MRCI progress
        lastline = 0
        for line in lines:
            lastline += 1
            if "Analysis of CPU times by interactions" in line:
                lastline -= 5
                break
        # identify final CI iteration
        iterstring = lines[lastline][:7]
        firstline = lastline
        while True:
            firstline -= 1
            if not lines[firstline][:7] == iterstring:
                firstline += 1
                break
        # extract CI energies
        energylines = range(firstline, lastline + 1)
        CCE = [] # current conformation energies
        for i in energylines:
            CCE.append(float(lines[i][50:62]))
        CIenergies.append(CCE)
        CIiterations.append(iterstring.replace(" ", ""))
    f.close()
    prog += 1

# produce list of distances from their files
distances = []
for file in geomfiles:
    cleaned = file[:-4]
    distances.append(cleaned)

# save data
# MCSCF
count = 0
f = open("MCenergies.csv", "w")
# write the MCSCF energies
for conformation in MCenergies:
    f.write(distances[count] + ', ')
    f.write(str(conformation)[1:-1])
    f.write('\n')
    count += 1
f.close()
count = 0
f = open("MCconvergences.csv", "w")
# write the convergences
for conformation in MCiterations:
    f.write(distances[count] + ', ')
    f.write(conformation)
    f.write('\n')
    count += 1
f.close()

# CI
if CI:
    count = 0
    f = open("CIenergies.csv", "w")
    # write the CI energies
    for conformation in CIenergies:
        f.write(distances[count] + ', ')
        f.write(str(conformation)[1:-1])
        f.write('\n')
        count += 1
    f.close()
    count = 0
    f = open("CIconvergences.csv", "w")
    # write the convergences
    for conformation in CIiterations:
        f.write(distances[count] + ', ')
        f.write(conformation)
        f.write('\n')
        count += 1
    f.close()

print("All done!")
