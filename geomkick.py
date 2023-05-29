# parameters
geoms_file = "eoms.txt" # Path to file with geometries
init_dir = "S-FINAL" # Path to directory with Columbus already inputted
parallel = True

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# read given geometry files
f = open(geoms_file, "r")
datafile = f.readlines()
f.close()
print("Input file read")

# dummy cartgrd
cartgrdtxt = """    0.739462D-07   0.107719D-01   0.359672D-02
  -0.637601D-07   0.573448D-03   0.113684D-01
  -0.408939D-07  -0.123975D-01  -0.519692D-02
   0.345788D-07  -0.168148D-02  -0.133691D-01
  -0.145659D-07   0.423517D-02   0.559146D-02
   0.106949D-07  -0.150151D-02  -0.199053D-02"""

# cart2int input
i2ctxt = """ &input
    calctype='int2cart'
 /"""

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
#SBATCH -n 24
#SBATCH -t 40:0:0
set -e
module list
$COLUMBUS/runc -m 80000 -nproc 24 > runls
cp WORK/ciudg.perf .
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=directory))
    g.close()

# prepare COLUMBUS for each step
def slurmcop(target, currgeom):
    str_target = str(target)[0:-1]
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
    g = open(str_target + '/intgeomch', "w")
    for i in currgeom:
        g.write(i)
    g.close()
    # generate dummy cartgrd
    f = open(str_target + "/cartgrd", "w")
    f.write(cartgrdtxt)
    f.close()
    # run cart2int to convert to Cartesians
    f = open(str_target + "/cart2intin", "w")
    f.write(i2ctxt)
    f.close()
    rv = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./"+str_target,capture_output=True)
    # replace geom with geom.new
    os.system("cp " + str_target + "/geom.new " + str_target + "/geom")

# main body of code
currgeom = []
currdir = ""
for line in datafile:
    if line[0] == " ":
        currgeom.append(line)
    elif currgeom == []:
        print("First line detected")
        currdir = line
    elif line[0] == "END":
        slurmcop(currdir, currgeom)
    else:
        slurmcop(currdir, currgeom)
        currdir = line
        currgeom = []
