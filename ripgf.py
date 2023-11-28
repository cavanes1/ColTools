# input if ab initio
#   [init_dir] - reference COLUMBUS input
#     contains [refcartfl] - reference Cartesian geometry, COLUMBUS format
#     contains intcfl - COLUMBUS internal coordinate file
#   Surfgen PES analysis
#     fit.in
#     intcfl
#     basis.in
#     Hd.CheckPoint

# parameters
refcartfl = "ORIGIN/geom" # Path of initial Cartesian geometry file
state = 1
ncoord = 12 # Number of internal coordinates
init_dir = "ORIGIN"

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# create geometry file
os.system("cp " + refcartfl + " ./geom.all")

# energy extraction function
def displace(target, ref = False):
    # get energy
    f = open(target + "/LISTINGS/ciudgsm.sp", "r")
    lines = f.readlines()
    f.close()
    energy = ""
    for line in lines:
        if "eci" in line:
            energy = line.split()[2]
            break

    # save energy
    if ref:
        filecmd = "w"
    else:
        filecmd = "a"
    f = open("energy.all", filecmd)
    f.write(energy + "\n")
    f.close()

# reference geometry
displace("E0",  True)
# single coordinate displacement
for i in range(ncoord):
    print("\ni = " + str(i + 1))
    target = "i" + str(i + 1)
    displace(target)
# pairwise coordinate displacements
for i in range(ncoord):
    for j in range(i, ncoord):
        print("\ni = " + str(i + 1) + "    j = " + str(j + 1))
        target = "i" + str(i + 1) + "j" + str(j + 1)
        displace(target)

# run gf.x
rv = subprocess.run(["./gf.x"],cwd="./",capture_output=True)
f = open("./gf.log", "w")
f.write(rv.stdout.decode('utf8'))
f.close()
print("gf.x completed")
print(rv.stdout.decode('utf8'))
