# module imports
import numpy as np
import os
print("modules imported")

# physical constants
file = "geom"

# conversion factor
conversion_factor = 1.889726125 # Bohr radii per angstrom

# equilibrium coordinates from NIST
Sx = 0.0000*conversion_factor
Sy = 0.0000*conversion_factor
Sz = 0.8622*conversion_factor
C2x = 0.0000*conversion_factor
C2y = 0.7421*conversion_factor
C2z = -0.7942*conversion_factor
C3x = 0.0000*conversion_factor
C3y = -0.7421*conversion_factor
C3z = -0.7942*conversion_factor
Hx = 0.9174*conversion_factor
Hy = 1.2493*conversion_factor
Hz = 1.0661*conversion_factor

# formatting numbers
zero = format(0, "14.8f")
C2x = format(C2x, "14.8f")
C2y = format(C2y, "14.8f")
C2z = format(C2z, "14.8f")
C3x = format(C3x, "14.8f")
C3y = format(C3y, "14.8f")
#C3z = format(C3z, "14.8f")
H4x = format(-Hx, "14.8f")
H4y = format(Hy, "14.8f")
H4z = format(-Hz, "14.8f")
H5x = format(Hx, "14.8f")
H5y = format(Hy, "14.8f")
H5z = format(-Hz, "14.8f")
H6x = format(Hx, "14.8f")
H6y = format(-Hy, "14.8f")
H6z = format(-Hz, "14.8f")
H7x = format(-Hx, "14.8f")
H7y = format(-Hy, "14.8f")
H7z = format(-Hz, "14.8f")
print("physical constants prepared")

# write two files
def write_files(directory = 'equil', RCS = Sz - C3z):
    Snew = format(C3z + RCS, "14.8f")
    os.system("mkdir " + directory)
    # write geometry file (Hydrogen order is H1, H2, H3)
    f = open(directory + '/' + file, "a")
    f.write(" S    16.0" + zero + zero + Snew + "   31.97207117\n")
    f.write(" C     6.0" + zero + C2y + C2z + "   12.00000000\n")
    f.write(" C     6.0" + zero + C3y + C2z + "   12.00000000\n")
    f.write(" H     1.0" + H4x + H4y + H4z + "    1.00782504\n")
    f.write(" H     1.0" + H5x + H5y + H5z + "    1.00782504\n")
    f.write(" H     1.0" + H6x + H6y + H6z + "    1.00782504\n")
    f.write(" H     1.0" + H7x + H7y + H7z + "    1.00782504\n")
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
write_files(directory = '3.10', RCS = 3.1) # 3.1301
print("all files written")

# delete .git directory
os.system("rm -rf .git")
print(".git directory deleted")
