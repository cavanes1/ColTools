# run slurmcop? and parameters
coordinate = "CS"
autocop = 'r'
leftmost = 1.5
rightmost = 15
start = 3.1 # initial geometry
# CS is 3.13 Bohr
step = 0.1 # spacing

# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# physical constants
file = "geom"
# angles in degrees
beta = 33.0

# converting to Bohr radii and radians
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

# for a single geometry
def write_files(directory = 'equil', RCS = Sz - C3z):
    Snew = format(C3z + RCS, "14.8f")
    # write geometry file
    f = open(directory + '/' + file, "w")
    f.write(" S    16.0" + zero + zero + Snew + "   31.97207117\n")
    f.write(" C     6.0" + zero + C2y + C2z + "   12.00000000\n")
    f.write(" C     6.0" + zero + C3y + C2z + "   12.00000000\n")
    f.write(" H     1.0" + H4x + H4y + H4z + "    1.00782504\n")
    f.write(" H     1.0" + H5x + H5y + H5z + "    1.00782504\n")
    f.write(" H     1.0" + H6x + H6y + H6z + "    1.00782504\n")
    f.write(" H     1.0" + H7x + H7y + H7z + "    1.00782504\n")
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

# use this function if running interactively
# submits the individual job to SLURM
def cop(source, target):
    str_source = format(source, ".2f")
    str_target = format(target, ".2f")
    print("running cop")
    print("   source = " + str_source)
    print("   target = " + str_target)
    # make list of bond length distances
    path = './'
    distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
    print("finished producing distance list")
    if '.git' in distances:
        distances.remove('.git')
        print(".git directory detected and ignored")
    # if target already exists
    if str_target in distances:
        os.system("rm -r " + str_target)
        print("!!! TARGET ALREADY EXISTS\nremoved old directory")
    # copy the equil folder's contents
    os.system("cp -r " + str_source + " " + str_target)
    print("folder's contents copied")
    # remove old slurm output(s)
    path = './' + str_target + "/"
    flist = [file for file in os.listdir(path) if os.path.isfile(path+file)]
    print("file list generated")
    for file in flist:
        if 'slurm' in file:
            os.system("rm " + path + file)
            print("deleted " + file)
    # produce the correct geom and slurm files
    if coordinate == "CS":
        write_files(directory = str_target, RCS = target)
    else:
        write_files(directory = str_target, RSH = target)
    print("geom and slurm files written")
    # Move old directory's orbitals into new directory
    os.system("cp " + str_source + "/MOCOEFS/mocoef_mc.sp " + str_target)
    print("mocoef_mc.sp moved")
    # Rename starting orbitals
    os.system("mv " + str_target + "/mocoef_mc.sp " + str_target + "/mocoef")
    print("mocoef renamed")
    # run Columbus by submitting to SLURM
    rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+str_target,capture_output=True)
    print(rv.stdout.decode('utf8'))

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
    if coordinate == "CS":
        write_files(directory = str_target, RCS = target)
    #else:
        #write_files(directory = str_target, PHHH = target)
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
