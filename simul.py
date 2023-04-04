# parameters
ID = "LST"
step = 0.04 # Step size
init_cart_name = "0/geom" # Path of initial Cartesian geometry file
final_cart_name = "geom" # Name of final Cartesian geometry file
parallel = True

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# read given Cartesian geometry files
f = open(init_cart_name, "r")
init_cart = f.readlines()
f.close()
f = open(final_cart_name, "r")
final_cart = f.readlines()
f.close()
print("Cartesian geometry files read")

# extract data from Cartesian geometries
init_cart_data = []
for line in init_cart:
    init_cart_data.append(line.split())
final_cart_data = []
for line in final_cart:
    final_cart_data.append(line.split())
print("Cartesian geometry data extracted")

# create directories
allitems = os.listdir(".")
if "FINAL" not in allitems:
    os.system("mkdir FINAL")
os.system("cp " + final_cart_name + " FINAL/geom")

# generate intcin
conv = 0.529177211 # Angstroms per Bohr radii
# initial geometry
f = open("0/intcin", "w")
f.write("TEXAS\n")
for atom in init_cart_data:
    f.write("  " + atom[0]
            + format(float(atom[1]), "17.5f")
            + format(float(atom[2])*conv, "10.5f")
            + format(float(atom[3])*conv, "10.5f")
            + format(float(atom[4])*conv, "10.5f") + "\n")
f.close()
# final geometry
f = open("FINAL/intcin", "w")
f.write("TEXAS\n")
for atom in final_cart_data:
    f.write("  " + atom[0]
            + format(float(atom[1]), "17.5f")
            + format(float(atom[2])*conv, "10.5f")
            + format(float(atom[3])*conv, "10.5f")
            + format(float(atom[4])*conv, "10.5f") + "\n")
f.close()
print("intcin generated")

# run intc to generate intcfl
# initial geometry
rv = subprocess.run(["/home/cavanes1/col/Columbus/intc.x"],cwd="./0",capture_output=True)
print("Initial intc output:")
print(rv.stdout.decode('utf8'))
# final geometry
rv = subprocess.run(["/home/cavanes1/col/Columbus/intc.x"],cwd="./FINAL",capture_output=True)
print("Final intc output:")
print(rv.stdout.decode('utf8'))

# generate internal coordinates from Cartesian coordinates
# generate cart2intin
c2itxt = """ &input
    calctype='cart2int'
 /"""
f = open("0/cart2intin", "w")
f.write(c2itxt)
f.close()
f = open("FINAL/cart2intin", "w")
f.write(c2itxt)
f.close()
# generate dummy cartgrd
cartgrdtxt = """    0.739462D-07   0.107719D-01   0.359672D-02
  -0.637601D-07   0.573448D-03   0.113684D-01
  -0.408939D-07  -0.123975D-01  -0.519692D-02
   0.345788D-07  -0.168148D-02  -0.133691D-01
  -0.145659D-07   0.423517D-02   0.559146D-02
   0.106949D-07  -0.150151D-02  -0.199053D-02"""
f = open("0/cartgrd", "w")
f.write(cartgrdtxt)
f.close()
f = open("FINAL/cartgrd", "w")
f.write(cartgrdtxt)
f.close()
# run cart2int
rv = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./0",capture_output=True)
rv2 = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./FINAL",capture_output=True)
print("Initial cart2int output:")
print(rv.stdout.decode('utf8'))
print("Final cart2int output:")
print(rv2.stdout.decode('utf8'))

# read internal coordinate files
f = open("0/intgeom", "r")
init_int = f.readlines()
f.close()
init_int_data = []
for line in init_int:
    init_int_data.append(float(line))
init_int_data = np.array(init_int_data)
f = open("FINAL/intgeom", "r")
final_int = f.readlines()
f.close()
final_int_data = []
for line in final_int:
    final_int_data.append(float(line))
final_int_data = np.array(final_int_data)
print("Internal geometry files read")

# create interpolation vector
interpvec = final_int_data - init_int_data
print("Interpolation vector created")

# reverse cart2intin direction in 0
i2ctxt = """ &input
    calctype='int2cart'
 /"""
f = open("0/cart2intin", "w")
f.write(i2ctxt)
f.close()
print("cart2intin direction reversed in initial geometry directory")

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
date""".format(name=ID+directory))
    else:
        g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 24
#SBATCH -t 40:0:0
set -e
module list
$COLUMBUS/runc -m 80000 -nproc 24 > runls
cp WORK/ciudg.perf .
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=ID+directory))
    g.close()

# run COLUMBUS for each step
def slurmcop(target):
    str_target = str(target)
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
    os.system("cp -r " + "0" + " " + str_target)
    print("copied " + "0" + " to " + str_target)
    # produce the correct SLURM file
    write_SLURM(str_target)
    # generate interpolated geometry as intgeomch
    f = open(str_target + "/intgeomch", "w")
    currgeom = init_int_data + interpvec*step*target
    for coord in currgeom:
        f.write(format(float(coord), "14.8f") + "\n")
    f.close()
    # run cart2int to convert to Cartesians
    rv = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./"+str_target,capture_output=True)
    #print("cart2int output:")
    #print(rv.stdout.decode('utf8'))
    # replace geom with geom.new
    os.system("cp " + str_target + "/geom.new " + str_target + "/geom")
    # Move old directory's orbitals into new directory and rename
    #os.system("cp " + str_source + "/MOCOEFS/mocoef_mc.sp " + str_target)
    #os.system("mv " + str_target + "/mocoef_mc.sp " + str_target + "/mocoef")
    # run Columbus
    rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+str_target,capture_output=True)
    print(rv.stdout.decode('utf8'))

# run copyfunction automatically
for i in range(int(1/step)):
    slurmcop(i + 1)
