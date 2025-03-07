# module imports
import numpy as np
import os
print("modules imported")

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

# write two files
def write_files(directory = 'equil', RPH = PH, PHHH = PHHHeq):
    H1x = format(RPH*np.cos(beta), "14.8f")
    H1z = format(-1*RPH*np.sin(beta), "14.8f")
    Hx = format(-1*PHHH*np.cos(gamma), "14.8f")
    Hz = format(-1*PHHH*np.sin(gamma), "14.8f")
    os.system("mkdir " + directory)
    # write geometry file (Hydrogen order is H1, H2, H3)
    f = open(directory + '/' + file, "a")
    f.write(" P    15.0" + zero + zero + zero + "   30.97376199\n")
    f.write(" H     1.0" + H1x + zero + H1z + "    1.00782504\n")
    f.write(" H     1.0" + Hx + H2y + Hz + "    1.00782504\n")
    f.write(" H     1.0" + Hx + H3y + Hz + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "a")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -c 1
#SBATCH -t 2:0:0
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

#write_files(directory = 'equil', RPH = PH, PHHH = PHHHeq)
write_files(directory = '2.70', RPH = 2.7, PHHH = PHHHeq)
write_files(directory = '18', RPH = PH, PHHH = 1.8)
print("all files written")

# delete .git directory
os.system("rm -rf .git")
print(".git directory deleted")
