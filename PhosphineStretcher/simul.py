# parameters
ID = "PH"
coordinate = "PH"
leftmost = 1.5
rightmost = 15
start = 2.7 # initial geometry
# PH is 2.68 Bohr, PHHH is 1.84 Bohr
step = 0.1 # spacing
parallel = False

# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# physical constants
file = "geom"
# angles in degrees
beta = 33.0

# converting to Bohr radii and radians
conversion_factor = 1.889726125 # Bohr radii per angstrom
PH = 2.6834
beta *= np.pi/180
square_root = 0.86602540378443864676 # sqrt(3)/2
planeprojectionPH = PH*np.cos(beta)
# equilibrium coordinates
Hxeq = -0.5*planeprojectionPH
H2y = square_root*planeprojectionPH
H3y = -1*square_root*planeprojectionPH
Hzeq = -1*PH*np.sin(beta)
PHHHeq = np.sqrt(Hxeq**2+Hzeq**2)
gamma = np.arctan(Hzeq/Hxeq)
# formatting numbers
zero = format(0, "14.8f")
H2y = format(H2y, "14.8f")
H3y = format(H3y, "14.8f")
print("physical constants prepared")

# for a single geometry
def write_files(directory = 'equil', RPH = PH, PHHH = PHHHeq):
    H1x = format(RPH*np.cos(beta), "14.8f")
    H1z = format(-1*RPH*np.sin(beta), "14.8f")
    Hx = format(-1*PHHH*np.cos(gamma), "14.8f")
    Hz = format(-1*PHHH*np.sin(gamma), "14.8f")
    # write geometry file (Hydrogen order is H, H1, H2, H3)
    f = open(directory + '/' + file, "w")
    f.write(" P    15.0" + zero + zero + zero + "   30.97376199\n")
    f.write(" H     1.0" + H1x + zero + H1z + "    1.00782504\n")
    f.write(" H     1.0" + Hx + H2y + Hz + "    1.00782504\n")
    f.write(" H     1.0" + Hx + H3y + Hz + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "w")
    if not parallel:
        g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -c 1
#SBATCH -t 20:0:0
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
#SBATCH -t 20:0:0

ulimit -s unlimited
module list
$COLUMBUS/runc -nproc 24 > runls
cp WORK/ciudg.perf .
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=ID+directory))
    g.close()

# this function runs the python script in SLURM
def slurmcop(target):
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
    if coordinate == "PH":
        write_files(directory = str_target, RPH = target)
    else:
        write_files(directory = str_target, PHHH = target)
    # run Columbus
    rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+str_target,capture_output=True)
    print(rv.stdout.decode('utf8'))

# run copyfunction automatically
allgeoms = np.arange(leftmost, rightmost + 0.001, step)
for gm in allgeoms:
    slurmcop(gm)
