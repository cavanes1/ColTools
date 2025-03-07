# run slurmcop? and parameters
autocop = 'r'
leftmost = -1
rightmost = 1
start = 0 # initial geometry
step = 0.05 # spacing

# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# extract data
f = open("0.00/geom", "r")
lines = f.readlines()
f.close()

# extract coordinates
oldgeom = []
for i in lines:
    temporary_list = i.split()[2:5]
    temporary_list = [float(i) for i in temporary_list]
    oldgeom.append(temporary_list)
oldgeom = np.array(oldgeom)
print("Initial (zero) geometry")
print(oldgeom)

# converting to Bohr radii and radians
conversion_factor = 1.889726125 # Bohr radii per angstrom

# ripped zero coordinates
N1x = oldgeom[0][0]
N1y = oldgeom[0][1]
N1z = oldgeom[0][2]
N2x = oldgeom[1][0]
N2y = oldgeom[1][1]
N2z = oldgeom[1][2]
N3x = oldgeom[2][0]
N3y = oldgeom[2][1]
N3z = oldgeom[2][2]
N4x = oldgeom[3][0]
N4y = oldgeom[3][1]
N4z = oldgeom[3][2]
Cx = oldgeom[4][0]
Cy = oldgeom[4][1]
Cz = oldgeom[4][2]
Hx = oldgeom[5][0]
Hy = oldgeom[5][1]
Hz = oldgeom[5][2]
print("zero coordinates ripped")

# for a single geometry
file = "geom"
def write_files(directory = 'equil', Ndisp = 0):
    # write geometry file
    f = open(directory + '/' + file, "w")
    f.write(" N     7.0" + format(N1x, "14.8f") + format(N1y, "14.8f") + format(N1z, "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + format(N1x, "14.8f") + format(N1y, "14.8f") + format(N1z, "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + format(N1x, "14.8f") + format(N1y, "14.8f") + format(N1z, "14.8f") + "   14.00307400\n")
    f.write(" N     7.0" + format(N1x + Ndisp, "14.8f") + format(N1y, "14.8f") + format(N1z, "14.8f") + "   14.00307400\n")
    f.write(" C     6.0" + format(Cx, "14.8f") + format(Cy, "14.8f") + format(Cz, "14.8f") + "   12.00000000\n")
    f.write(" H     1.0" + format(Hx, "14.8f") + format(Hy, "14.8f") + format(Hz, "14.8f") + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "w")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -c 1
#SBATCH -t 24:0:0
set -e
module list
$COLUMBUS/runc > runls
rm -r WORK
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=directory))
    g.close()

# this function runs the python script in SLURM
def slurmcop(source, target):
    str_source = format(source, ".2f")
    str_target = format(target, ".2f")
    # make list of bond length distances
    path = './'
    distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
    if '.git' in distances:
        distances.remove('.git')
    # if target already exists
    if str_target in distances:
        print("!!!!!!!!!!!!TARGET ALREADY EXISTS")
        os.system("rm -r " + str_target)
    # copy the equil folder's contents
    os.system("cp -r " + str_source + " " + str_target)
    print("copied " + str_source + " to " + str_target)
    # remove old slurm output(s)
    path = './' + str_target + "/"
    flist = [file for file in os.listdir(path) if os.path.isfile(path+file)]
    for file in flist:
        if 'slurm' in file:
            os.system("rm " + path + file)
    # produce the correct geom and slurm files
    write_files(directory = str_target, Ndisp = target)
    # Move old directory's orbitals into new directory
    os.system("cp " + str_source + "/MOCOEFS/mocoef_mc.sp " + str_target)
    # Rename starting orbitals
    os.system("mv " + str_target + "/mocoef_mc.sp " + str_target + "/mocoef")
    # run Columbus interactivelyish
    rv = subprocess.run(["/home/cavanes1/col/Columbus/runc"],cwd="./"+str_target,capture_output=True)
    # save results to runls
    h = open(str_target + '/runls', "w")
    h.write(rv.stdout.decode('utf8'))
    h.close()
    # remove WORK directory
    os.system("rm -r " + str_target + "/WORK")

# run copyfunction automatically
if autocop == 'r':
    right = np.arange(start + step, rightmost + 0.001, step)
    for gm in right:
        slurmcop(gm - step, gm)

if autocop == 'l':
    left = np.arange(start - step, leftmost - 0.001, -step)
    for gm in left:
        slurmcop(gm + step, gm)

# fill in gaps
if autocop == 'rf':
    i = float(sys.argv[1])
    right = [i + step, i + step*2, i + step*3, i + step*4, i + step*5]
    for gm in right:
        slurmcop(gm - step, gm)

if autocop == 'lf':
    i = float(sys.argv[1])
    right = [i - step, i - step*2, i - step*3, i - step*4]
    for gm in right:
        slurmcop(gm + step, gm)
