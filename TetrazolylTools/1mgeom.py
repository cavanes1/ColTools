# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# internal coordinates
zero = format(0, "14.8f")
CH = 1.07313
CN = 1.34152
NN = 1.24474
HCN = 125.49162
CNN = 109.32971

# converting to Bohr radii and radians
conversion_factor = 1.889726125 # Bohr radii per angstrom
CH *= conversion_factor
CN *= conversion_factor
NN *= conversion_factor
HCN *= np.pi/180
CNN *= np.pi/180

# Cartesian coordinates
N1y = CN*np.sin(HCN)
N1z = CN*np.cos(HCN)
N3y = N1y - NN*np.cos(CNN - HCN + np.pi/2)
N3z = N1z - NN*np.sin(CNN - HCN + np.pi/2)

# for a single geometry
file = "geom"
def write_files():
    # write geometry file
    f = open(file, "w")
    f.write(" N     7.0" + zero + format(-1*N1y, "14.8f") + format(N1z, "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + zero + format(N1y, "14.8f") + format(N1z, "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + zero + format(-1*N3y, "14.8f") + format(N3z, "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + zero + format(N3y, "14.8f") + format(N3z, "14.8f") + "   14.00307400\n")
    f.write(" C     6.0" + zero + zero + zero + "   12.00000000\n")
    f.write(" H     1.0" + zero + zero + format(CH, "14.8f") + "    1.00782504\n")
    f.close()

write_files()
