# module import
import numpy as np
import os

# make list of carbon-Hplane distances
path = './'
distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
if '.git' in distances:
    distances.remove('.git')
if 'SLURM' in distances:
    distances.remove('SLURM')
if 'SH' in distances:
    distances.remove('SH')

energies = []
convergences = []
iterations = []

prog = 0
for distance in distances:
    f = open(distance + "/LISTINGS/mcscfsm.sp", "r")
    lines = f.readlines()
    CCE = [] # current conformation energies
    # line with --- on top of energies
    firstline = 0
    # line with --- below energies
    lastline = 0
    count = 0 # current line
    # go through all lines in the file
    for line in lines:
        if line[3:4] == '-':
            # if we haven't encountered --- yet
            if firstline == 0:
                # this is the top
                firstline = count + 1
            # if we have already seen ---
            else:
                # this is the bottom
                lastline = count - 1
                break
        # we're done with this line, onto the next
        count += 1
    # determine whether it has converged
    convline = 0
    count = 0
    for line in lines:
        if line[1:2] == 'f':
            convline = count + 1
            break
        count += 1
    # between the --- lines
    for i in range(firstline, lastline + 1):
        # add all the energies
        CCE.append(float(lines[i][47:61]))
    energies.append(CCE)
    convergences.append(lines[convline][74:83])
    iterations.append(str(int(lines[convline][2:5])))
    f.close()
    # print current progress
    prog += 1
    print(str(prog) + ' of ' + str(len(distances)))

count = 0
f = open("allenergies.csv", "w")
# write the energies
for conformation in energies:
    if "n" in distances[count]:
        f.write("-" + distances[count][1:] + ', ')
    else:
        f.write(distances[count] + ', ')
    f.write(str(conformation)[1:-1])
    f.write('\n')
    count += 1
count = 0
f = open("convergences.csv", "w")
# write the convergences
for conformation in convergences:
    if "n" in distances[count]:
        f.write("-" + distances[count][1:] + ', ')
    else:
        f.write(distances[count] + ', ')
    f.write(conformation + ', ')
    f.write(iterations[count])
    f.write('\n')
    count += 1
f.close()
