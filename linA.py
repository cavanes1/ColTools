# parameters
ID = "LIN"
r = 0.1 # radius of loop in units of g/h - Bohr?
step = 1 # Step size/pi in radians
direc = "12CI"
parallel = True

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# read from polyhesls
f = open(direc + "/LISTINGS/polyhesls.all", "r")
lines = f.readlines()
f.close()
print("Data read from polyhesls")

# extract data from polyhesls
position = 0
iteration = 0
read_geom = False
cartzone = False
read_g = False
read_h = False
data = []
for line in lines:
    if "iteration" in line:
        iteration = int(line.split()[3])
        data.append([iteration,[],[],[]])
    if line == "\n":
        read_geom = False
        read_h = False
    if read_geom:
        data[-1][1].append(line.split())
    if "GEOMETRY" in line:
        read_geom = True
    if "cartesian" in line:
        cartzone = True
    if "internal" in line:
        cartzone = False
        read_g = False
    if cartzone:
        if "HR=" in line:
            read_h = True
        if "GR=" in line:
            read_g = True
        if read_h:
            data[-1][3].append(line.split()[-3:])
        if read_g:
            data[-1][2].append(line.split()[-3:])
print("Data extracted from polyhesls")

# extract data from Cartesian geometry to obtain its structure
f = open(direc + "/geom", "r")
cart = f.readlines()
f.close()
cart_data = []
for line in cart:
    cart_data.append(line.split())
print("Cartesian geometry structure data extracted")

# select polyhesls iteration to use
print("List of iterations:")
for iteration in range(len(data)):
    print("Choice " + str(iteration) + ": "  + str(data[iteration][0]))
choseniter = input("Use which iteration? (Enter choice code.) ")
cdata = data[int(choseniter)]

# create origin geometry vector
O = []
for triplet in cdata[1]:
    for entry in triplet[1:]:
        O.append(float(entry))
O = np.array(O)
print("\norigin geometry vector")
print(O)
# create x and y vectors
g = []
for triplet in cdata[2]:
    for entry in triplet:
        g.append(float(entry[:-1]))
g = np.array(g)
print("\ng vector")
print(g)
h = []
for triplet in cdata[3]:
    for entry in triplet:
        h.append(float(entry[:-1]))
h = np.array(h)
print("\nh vector")
print(h)
x = g/np.linalg.norm(g)
print("\nx vector (normalized g)")
print(x)
y = h/np.linalg.norm(h)
print("\ny vector (normalized h)")
print(y)
print("Orthogonal intersection adapted coordinate unit vectors created")

# function to write SLURM script
def write_SLURM(directory):
    g = open(directory + '/script.sh', "w")
    if not parallel:
        g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 2:0:0
set -e
module list
$COLUMBUS/runc > runls
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=ID+directory))
    else:
        g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 24
#SBATCH -t 40:0:0
set -e
module list
$COLUMBUS/runc -m 80000 -nproc 24 > runls
cp WORK/ciudg.perf .
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=ID+directory))
    g.close()

# function to write geometry
def write_geom(directory):
    target = int(directory)
    theta = step*target*np.pi
    print("Theta = " + str(theta))
    currgeom = O + r*np.cos(theta)*x + r*np.sin(theta)*y
    g = open(directory + '/geom', "w")
    atom_number = 0
    for atom in cart_data:
        g.write(" " + atom[0]
                + format(float(atom[1]), "8.1f")
                + format(float(currgeom[atom_number]), "14.8f")
                + format(float(currgeom[atom_number + 1]), "14.8f")
                + format(float(currgeom[atom_number + 2]), "14.8f")
                + format(float(atom[5]), "14.8f")
                + "\n")
        atom_number += 3
    g.close()

# run COLUMBUS for each step
def slurmcop(target):
    str_target = str(target)
    # make list of existing directories
    path = './'
    distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
    if '.git' in distances:
        distances.remove('.git')
    # if target already exists
    if str_target in distances:
        print("!!!!!!!!!!!!TARGET ALREADY EXISTS")
        os.system("rm -r " + str_target)
    # copy the source folder's contents
    os.system("cp -r " + direc + " " + str_target)
    print("copied " + direc + " to " + str_target)
    # produce the correct SLURM file
    write_SLURM(str_target)
    # produce geometry
    write_geom(str_target)
    # Move old directory's orbitals into new directory and rename
    os.system("cp " + direc + "/MOCOEFS/mocoef_mc.sp " + str_target)
    os.system("mv " + str_target + "/mocoef_mc.sp " + str_target + "/mocoef")
    # run Columbus
    rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+str_target,capture_output=True)
    print(rv.stdout.decode('utf8'))

# run copyfunction automatically
for i in range(int(2/step)):
    slurmcop(i + 1)
