# input if surface
#   [refcartfl] - reference Cartesian geometry, COLUMBUS format
#   intcfl - COLUMBUS internal coordinate file
# input if ab initio
#   [init_dir] - reference COLUMBUS input
#     contains [refcartfl] - reference Cartesian geometry, COLUMBUS format
#     contains intcfl - COLUMBUS internal coordinate file
# usage notes
#   if doing ab initio, use rerun.py afterwards in order to run COLUMBUS jobs

# parameters
refcartfl = "ORIGIN/geom" # Path of initial Cartesian geometry file
state = 1
ncoord = 12 # Number of internal coordinates
distcs = [1, 2, 3, 4, 9, 10] # coordinates which are bond distances
surface = False # False if ab initio
init_dir = "ORIGIN"
parallel = True

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# read reference point Cartesian geometry file
f = open(refcartfl, "r")
refcart = f.readlines()
f.close()
print("Cartesian geometry file read from " + refcartfl)

# extract data from Cartesian geometry
refcartdat = []
for line in refcart:
    refcartdat.append(line.split())
print("Cartesian geometry data extracted")

# create directories
allitems = os.listdir(".")
if "GFWORK" not in allitems:
    os.system("mkdir GFWORK")
    print("Work directory created")
else:
    print("Work directory already exists")
os.system("cp " + refcartfl + " GFWORK/geom")
if surface:
    os.system("cp intcfl GFWORK")
else:
    os.system("cp " + init_dir + "/intcfl GFWORK")

# generate internal coordinates from Cartesian coordinates
# generate cart2intin
c2itxt = """ &input
    calctype='cart2int'
 /"""
f = open("GFWORK/cart2intin", "w")
f.write(c2itxt)
f.close()
# generate dummy cartgrd
cartgrdtxt = """    0.739462D-07   0.107719D-01   0.359672D-02
  -0.637601D-07   0.573448D-03   0.113684D-01
  -0.408939D-07  -0.123975D-01  -0.519692D-02
   0.345788D-07  -0.168148D-02  -0.133691D-01
  -0.145659D-07   0.423517D-02   0.559146D-02
   0.106949D-07  -0.150151D-02  -0.199053D-02"""
f = open("GFWORK/cartgrd", "w")
f.write(cartgrdtxt)
f.close()
# run cart2int
rv = subprocess.run(["/home/cavanes1/C/columbus-v7.2/Columbus/cart2int.x"],cwd="./GFWORK",capture_output=True)
print("cart2int output:")
print(rv.stdout.decode('utf8'))

# read internal coordinate file
f = open("GFWORK/intgeom", "r")
refint = f.readlines()
f.close()
refintdat = []
print("Internal geometry file of reference point:")
for line in refint:
    print(line)
    refintdat.append(float(line))
refintdat = np.array(refintdat)

# reverse cart2intin direction
i2ctxt = """ &input
    calctype='int2cart'
 /"""
f = open("GFWORK/cart2intin", "w")
f.write(i2ctxt)
f.close()
print("cart2intin direction reversed in work directory")

# function to write SLURM script
def write_SLURM(directory):
    g = open(directory + '/script.sh', "w")
    if not parallel:
        g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 2:0:0
set -e
module list
$COLUMBUS/runc > runls
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=directory))
    else:
        g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -t 24:0:0
set -e
module list
$COLUMBUS/runc -m 160000 -nproc 48 > runls
cp WORK/ciudg.perf .
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=directory))
    g.close()

def slurmcop(target, currgeom):
    str_target = target
    print(str_target)
    # make list of bond length distances
    path = './'
    distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
    if '.git' in distances:
        distances.remove('.git')
    # if target already exists
    if str_target in distances:
        print("!!!!!!!!!!!!TARGET ALREADY EXISTS")
        os.system("rm -r " + str_target)
    # copy the source folder's contents
    os.system("cp -r " + init_dir + " " + str_target)
    print("copied " + init_dir + " to " + str_target)
    # produce the correct SLURM file
    write_SLURM(str_target)
    # copy new geometry
    g = open(str_target + '/geom', "w")
    for i in currgeom:
        g.write(i)
    g.close()

# function that generates the displacements
def displace(currgeom, target, ref = False):
    print("Generating displacement for internal coordinate geometry")
    # generate interpolated geometry as intgeomch
    f = open("GFWORK/intgeomch", "w")
    for coord in currgeom:
        print(coord)
        f.write(format(float(coord), "14.8f") + "\n")
    f.close()
    # run cart2int to convert to Cartesians
    rv = subprocess.run(["/home/cavanes1/C/columbus-v7.2/Columbus/cart2int.x"],cwd="./GFWORK",capture_output=True)
    #print("cart2int output:")
    #print(rv.stdout.decode('utf8'))
    # read displacement Cartesian geometry
    f = open("GFWORK/geom.new", "r")
    dispgeom = f.readlines()
    f.close()
    if surface:
        # save geometry
        if ref:
            filecmd = "w"
        else:
            filecmd = "a"
        f = open("geom.all", filecmd)
        for coord in dispgeom:
            f.write(coord)
        f.close()
    else:
        slurmcop(target, dispgeom)

# generate displacements
ainau = 0.000529177210903 # angstroms per 0.001 a0
# reference geometry
displace(refintdat, "E0",  True)
# single coordinate displacement
for i in range(ncoord):
    print("\ni = " + str(i + 1))
    currgeom = refintdat.copy()
    if i+1 in distcs:
        currgeom[i] += ainau
    else:
        currgeom[i] += 0.001
    target = "i" + str(i + 1)
    displace(currgeom, target)
# pairwise coordinate displacements
for i in range(ncoord):
    for j in range(i, ncoord):
        print("\ni = " + str(i + 1) + "    j = " + str(j + 1))
        currgeom = refintdat.copy()
        if i+1 in distcs:
            currgeom[i] += ainau
        else:
            currgeom[i] += 0.001
        if j+1 in distcs:
            currgeom[j] += ainau
        else:
            currgeom[j] += 0.001
        target = "i" + str(i + 1) + "j" + str(j + 1)
        displace(currgeom, target)

if surface:
    # run dat.x
    rv = subprocess.run(["./dat.x"],cwd="./",capture_output=True)
    f = open("./dat.log", "w")
    f.write(rv.stdout.decode('utf8'))
    f.close()
    print("dat.x completed")
    
    # filtering out only the energies of the state of interest
    f = open("fitener.dat", "r")
    dateners = f.readlines()
    f.close()
    f = open("energy.all", "w")
    for geometry in dateners:
        # subtract reference energy (from fit.in)
        thisE = str(float(geometry.split()[state - 1])/219474.63067-256.787847331183)
        f.write(thisE + "\n")
    f.close()
    print("Finished ripping fitener.dat to energy.all")
    
    # run gf.x
    rv = subprocess.run(["./gf.x"],cwd="./",capture_output=True)
    f = open("./gf.log", "w")
    f.write(rv.stdout.decode('utf8'))
    f.close()
    print("gf.x completed")
    print(rv.stdout.decode('utf8'))
