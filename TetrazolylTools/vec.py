# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# extract A
Afile = input("Name of initial directory: ")
f = open(Afile + "/geom", "r")
lines = f.readlines()
f.close()

A = []
for i in lines:
    temporary_list = i.split()[2:5]
    temporary_list = [float(i) for i in temporary_list]
    A.append(temporary_list)
A = np.array(A)
print("Initial (A) geometry")
print(A)

# extract V
Vfile = input("Name of file with direction: ")
f = open(Vfile, "r")
lines = f.readlines()
f.close()

V = []
for i in lines:
    temporary_list = i.split(",")[0:3]
    temporary_list = [float(i) for i in temporary_list]
    V.append(temporary_list)
V = np.array(V)
print("V direction: ")
print(V)

# ask for b
b = float(input("Step size: "))

# for a single geometry
def write_files(A, V, n, b):
    directory = str(n*b)
    # produce new geometry
    G = A.astype(np.float) + n*b*V.astype(np.float)
    print(G)
    # write geometry file
    f = open(directory + '/geom', "w")
    f.write(" N     7.0" + format(G[0][0], "14.8f") + format(G[0][1], "14.8f") + format(G[0][2], "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + format(G[1][0], "14.8f") + format(G[1][1], "14.8f") + format(G[1][2], "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + format(G[2][0], "14.8f") + format(G[2][1], "14.8f") + format(G[2][2], "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + format(G[3][0], "14.8f") + format(G[3][1], "14.8f") + format(G[3][2], "14.8f") + "   14.00307400\n")
    f.write(" C     6.0" + format(G[4][0], "14.8f") + format(G[4][1], "14.8f") + format(G[4][2], "14.8f") + "   12.00000000\n")
    f.write(" H     1.0" + format(G[5][0], "14.8f") + format(G[5][1], "14.8f") + format(G[5][2], "14.8f") + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "w")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -t 2:0:0
set -e
module list
$COLUMBUS/runc -m 160000 -nproc 48 > runls
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=directory))
    g.close()

# make copies
SC = int(input("Number of steps: "))
for i in range(SC + 1):
    target = str(i*b)
    # copy the equil folder's contents
    os.system("cp -r " + Afile + " " + target)
    print("copied " + Afile + " to " + target)

    write_files(A, V, i, b)
    rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+target,capture_output=True)
    print(rv.stdout.decode('utf8'))
