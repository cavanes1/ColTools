# module imports
import numpy as np
import os
print("modules imported")

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
print("physical constants prepared")

# write two files
def write_files(directory = '0.00', stretch = 0):
    stretch = format(stretch, "14.8f")
    os.system("mkdir " + directory)
    # write geometry file
    f = open(directory + '/' + file, "a")
    f.write(" C     6.0" + zero + zero + stretch + "   12.00000000\n")
    f.write(" H     1.0" + neg_half + pos_y + zero + "    1.00782504\n")
    f.write(" H     1.0" + neg_half + neg_y + zero + "    1.00782504\n")
    f.write(" H     1.0" + EBD + zero + zero + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "a")
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
date""".format(name=directory))
    g.close()
    os.system("cp makscfky " + directory)
    os.system("cp makmcky " + directory)
    os.system("cp cidrtplky " + directory)

write_files()
print("all files written")

# delete .git directory
os.system("rm -rf .git")
print(".git directory deleted")
