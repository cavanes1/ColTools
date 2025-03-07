# module imports
import numpy as np
import os
print("modules imported")

# physical constants
file = "geom"
# equilibrium coordinates from NIST
conversion_factor = 1.889726125 # Bohr radii per angstrom
# converting from Angstroms to Bohr radii
Cx = 0.6147*conversion_factor
Cy = 1.0867*conversion_factor
Cz = 0.8571*conversion_factor
Nx = 1.9021*conversion_factor
Ny = 1.7634*conversion_factor
Nz = 1.0319*conversion_factor
# attached to C
H1x = 0.0879*conversion_factor
H1y = 1.5325*conversion_factor
H1z = 0.0061*conversion_factor
H2x = 0.6641*conversion_factor
H2y = -0.0036*conversion_factor
H2z = 0.6869*conversion_factor
H3x = -0.0036*conversion_factor
H3y = 1.2570*conversion_factor
H3z = 1.7453*conversion_factor
# attached to N
H4x = 2.4036*conversion_factor
H4y = 1.3486*conversion_factor
H4z = 1.8155*conversion_factor
H5x = 2.4869*conversion_factor
H5y = 1.6039*conversion_factor
H5z = 0.2133*conversion_factor

# translating C to origin
Nx -= Cx
Ny -= Cy
Nz -= Cz
H1x -= Cx
H1y -= Cy
H1z -= Cz
H2x -= Cx
H2y -= Cy
H2z -= Cz
H3x -= Cx
H3y -= Cy
H3z -= Cz
H4x -= Cx
H4y -= Cy
H4z -= Cz
H5x -= Cx
H5y -= Cy
H5z -= Cz
Cx -= Cx
Cy -= Cy
Cz -= Cz

# equilibrium C-N bond distance
CNeq = np.sqrt(Nx**2 + Ny**2 + Nz**2)

# formatting numbers
Cx = format(Cx, "14.8f")
Cy = format(Cy, "14.8f")
Cz = format(Cz, "14.8f")
H1x = format(H1x, "14.8f")
H1y = format(H1y, "14.8f")
H1z = format(H1z, "14.8f")
H2x = format(H2x, "14.8f")
H2y = format(H2y, "14.8f")
H2z = format(H2z, "14.8f")
H3x = format(H3x, "14.8f")
H3y = format(H3y, "14.8f")
H3z = format(H3z, "14.8f")
print("physical constants prepared")

# write two files
def write_files(directory = 'equil', CN = CNeq):
    aNx = CN*Nx/CNeq
    aNy = CN*Ny/CNeq
    aNz = CN*Nz/CNeq
    aH4x = H4x + aNx - Nx
    aH4y = H4y + aNy - Ny
    aH4z = H4z + aNz - Nz
    aH5x = H5x + aNx - Nx
    aH5y = H5y + aNy - Ny
    aH5z = H5z + aNz - Nz
    # formatting numbers
    fNx = format(aNx, "14.8f")
    fNy = format(aNy, "14.8f")
    fNz = format(aNz, "14.8f")
    fH4x = format(aH4x, "14.8f")
    fH4y = format(aH4y, "14.8f")
    fH4z = format(aH4z, "14.8f")
    fH5x = format(aH5x, "14.8f")
    fH5y = format(aH5y, "14.8f")
    fH5z = format(aH5z, "14.8f")
    os.system("mkdir " + directory)
    # write geometry file (Hydrogen order is H, H1, H2, H3)
    f = open(directory + '/' + file, "a")
    f.write(" C     6.0" + Cx + Cy + Cz + "   12.00000000\n")
    f.write(" N     7.0" + fNx + fNy + fNz + "   14.00307400\n")
    f.write(" H     1.0" + H1x + H1y + H1z + "    1.00782504\n")
    f.write(" H     1.0" + H2x + H2y + H2z + "    1.00782504\n")
    f.write(" H     1.0" + H3x + H3y + H3z + "    1.00782504\n")
    f.write(" H     1.0" + fH4x + fH4y + fH4z + "    1.00782504\n")
    f.write(" H     1.0" + fH5x + fH5y + fH5z + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "a")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -c 1
#SBATCH -t 5:0:0
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
