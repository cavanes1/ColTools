# module import
import numpy as np
import os

# make list of bond length distances
path = './'
distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
if '.git' in distances:
    distances.remove('.git')
if 'SLURM' in distances:
    distances.remove('SLURM')
if 'SH' in distances:
    distances.remove('SH')
if 'equil' in distances:
    distances.remove('equil')
# directories without ciudgsm.sp will be removed from this list
good_distances = distances.copy()

energies = []
convergences = []
iterations = []

prog = 0
for distance in distances:
    path = "./" + distance + "/LISTINGS"
    flist = os.listdir(path)
    if "ciudgsm.sp" not in flist:
        print("The " + distance + " directory does not contain ciudgsm.sp")
        good_distances.remove(distance)
        continue
    f = open(distance + "/LISTINGS/ciudgsm.sp", "r")
    lines = f.readlines()
    CCE = [] # current conformation energies
    # line with --- on top of energies
    firstline = 0
    # line with --- below energies
    lastline = 0
    count = 0 # current line
    # go through all lines in the file
    first_time = 0
    for line in lines:
        if line[1:3] == 'fi':
            # if we haven't encountered "final" yet
            if first_time == 0:
                # this is BS
                first_time = 1
            # if we have already encountered "final"
            elif first_time == 1:
                # this is legit
                first_time = 2
                firstline = count + 1
        elif first_time == 2:
                if line[1:3] == '':
                    # this is the end
                    lastline = count - 1
                    break
        # we're done with this line, onto the next
        count += 1
    # determine whether it has converged
    convline = firstline - 3
    # between the --- lines
    for i in range(firstline, lastline + 1):
        # add all the energies
        CCE.append(float(lines[i][19:34]))
    energies.append(CCE)
    convergences.append(lines[convline][31:40])
    iterations.append(str(int(lines[lastline][10:14])))
    f.close()
    # print current progress
    prog += 1
    print(str(prog) + ' of ' + str(len(good_distances)))

count = 0
f = open("CIallenergies.csv", "w")
# write the energies
for conformation in energies:
    if "n" in good_distances[count]:
        f.write("-" + good_distances[count][1:] + ', ')
    else:
        f.write(good_distances[count] + ', ')
    f.write(str(conformation)[1:-1])
    f.write('\n')
    count += 1
count = 0
f = open("CIconvergences.csv", "w")
# write the convergences
for conformation in convergences:
    if "n" in good_distances[count]:
        f.write("-" + good_distances[count][1:] + ', ')
    else:
        f.write(good_distances[count] + ', ')
    f.write(conformation + ', ')
    f.write(iterations[count])
    f.write('\n')
    count += 1
f.close()

# print additional but unnecessary information
print("distances:")
print(distances)
print("good_distances:")
print(good_distances)
print("energies:")
print(energies)
print("convergences:")
print(convergences)
