# module imports
import numpy as np
import os
print("modules imported")

# physical constants
file = "geom"
# bond lengths in Angstroms
CS = 1.85908
SH = 1.35167
CH1 = 1.08334
CH2 = 1.08254
# angles in degrees
CSH = 96.40321
SCH1 = 106.06354
SCH23 = 127.65858
H2CH3 = 110.97987

# converting to Bohr radii and radians
conversion_factor = 1.889726125 # Bohr radii per angstrom
CS *= conversion_factor
SH *= conversion_factor
CH1 *= conversion_factor
CH2 *= conversion_factor
CSH *= np.pi/180
SCH1 *= np.pi/180
SCH23 *= np.pi/180
H2CH3 *= np.pi/180
CH23 = CH2*np.cos(H2CH3/2)
# equilibrium coordinates
H1x = -1*CH1*np.cos(np.pi-SCH1)
H1y = CH1*np.sin(np.pi-SCH1)
H2x = -1*CH23*np.cos(np.pi-SCH23)
H2y = -1*CH23*np.sin(np.pi-SCH23)
H2z = CH2*np.sin(H2CH3/2)
H3z = -1*H2z
# formatting numbers
zero = format(0, "14.8f")
H1x = format(H1x, "14.8f")
H1y = format(H1y, "14.8f")
H2x = format(H2x, "14.8f")
H2y = format(H2y, "14.8f")
H2z = format(H2z, "14.8f")
H3z = format(H3z, "14.8f")
print("physical constants prepared")

# write two files
def write_files(directory = 'equil', RCS = CS, RSH = SH):
    Hx = format(RSH*np.cos(np.pi-CSH) + RCS, "14.8f") # RSH + RCS if linear
    Hy = format(-1*RSH*np.sin(np.pi-CSH), "14.8f") # zero if linear
    RCS = format(RCS, "14.8f")
    os.system("mkdir " + directory)
    # write geometry file (Hydrogen order is H, H1, H2, H3)
    f = open(directory + '/' + file, "a")
    f.write(" S    16.0" + RCS + zero + zero + "   31.97207117\n")
    f.write(" C     6.0" + zero + zero + zero + "   12.00000000\n")
    f.write(" H     1.0" + Hx + Hy + zero + "    1.00782504\n")
    f.write(" H     1.0" + H1x + H1y + zero + "    1.00782504\n")
    f.write(" H     1.0" + H2x + H2y + H2z + "    1.00782504\n")
    f.write(" H     1.0" + H2x + H2y + H3z + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "a")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
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
