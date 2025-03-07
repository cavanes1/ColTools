# parameters
ID = "SM"
leftmost = -5
rightmost = 5
start = "0.00" # must be string
step = 0.1 # spacing

# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# physical constants
file = "geom"
equilibrium_BD = 1.079 # angstroms
conversion_factor = 1.889726125 # Bohr radii per angstrom
converted_EBD = equilibrium_BD*conversion_factor
EBD = format(converted_EBD, "14.8f")
zero = format(0, "14.8f")
neg_half = format(-0.5*converted_EBD, "14.8f")
square_root = 0.86602540378443864676 # sqrt(3)/2
pos_y = format(square_root*converted_EBD, "14.8f")
neg_y = format(-1*square_root*converted_EBD, "14.8f")
# distorted
Dneg_y = format(-1.69, "14.8f")
Dzero = format(0.5, "14.8f")
print("physical constants prepared")

# for a single geometry
def write_files(directory = '0.00', stretch = 0):
    stretch = format(stretch, "14.8f")
    # write geometry file
    f = open(directory + '/' + file, "w")
    f.write(" C     6.0" + zero + zero + stretch + "   12.00000000\n")
    f.write(" H     1.0" + neg_half + pos_y + zero + "    1.00782504\n")
    f.write(" H     1.0" + neg_half + neg_y + zero + "    1.00782504\n")
    f.write(" H     1.0" + EBD + zero + zero + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "w")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p shared
#SBATCH -c 1
#SBATCH -t 72:0:0
set -e
module list
$COLUMBUS/runc > runls
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=ID+directory))
    g.close()

# this function runs the python script in SLURM
def slurmcop(target):
    if target < 0:
        str_target = "n" + format(abs(target), ".2f")
    else:
        str_target = format(target, ".2f")
    # make list of bond length distances
    path = './'
    distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
    if '.git' in distances:
        distances.remove('.git')
    # if target already exists
    if str_target in distances:
        print("!!!!!!!!!!!!TARGET ALREADY EXISTS")
        os.system("rm -r " + str_target)
    # copy the starting folder's contents
    os.system("cp -r " + start + " " + str_target)
    print("copied " + start + " to " + str_target)
    # produce the correct geom and slurm files
    write_files(str_target, target)
    # run Columbus
    rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+str_target,capture_output=True)
    print(rv.stdout.decode('utf8'))

# run copyfunction automatically
allgeoms = np.arange(leftmost, rightmost + 0.001, step)
for gm in allgeoms:
    slurmcop(gm)