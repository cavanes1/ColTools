# run slurmcop? and parameters
coordinate = "PH"
autocop = 'r'
leftmost = 1.5
rightmost = 15
start = 2.7 # initial geometry
# PH is 2.68 Bohr, PHHH is 1.84 Bohr
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
PH = 2.6834
beta *= np.pi/180
square_root = 0.86602540378443864676 # sqrt(3)/2
planeprojectionPH = PH*np.cos(beta)
# equilibrium coordinates
Hxeq = -0.5*planeprojectionPH
H2y = square_root*planeprojectionPH
H3y = -1*square_root*planeprojectionPH
Hzeq = -1*PH*np.sin(beta)
PHHHeq = np.sqrt(Hxeq**2+Hzeq**2)
gamma = np.arctan(Hzeq/Hxeq)
# formatting numbers
zero = format(0, "14.8f")
H2y = format(H2y, "14.8f")
H3y = format(H3y, "14.8f")
print("physical constants prepared")

# for a single geometry
def write_files(directory = 'equil', RPH = PH, PHHH = PHHHeq):
    H1x = format(RPH*np.cos(beta), "14.8f")
    H1z = format(-1*RPH*np.sin(beta), "14.8f")
    Hx = format(-1*PHHH*np.cos(gamma), "14.8f")
    Hz = format(-1*PHHH*np.sin(gamma), "14.8f")
    # write geometry file (Hydrogen order is H1, H2, H3)
    f = open(directory + '/' + file, "w")
    f.write(" P    15.0" + zero + zero + zero + "   30.97376199\n")
    f.write(" H     1.0" + H1x + zero + H1z + "    1.00782504\n")
    f.write(" H     1.0" + Hx + H2y + Hz + "    1.00782504\n")
    f.write(" H     1.0" + Hx + H3y + Hz + "    1.00782504\n")
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
    if coordinate == "PH":
        write_files(directory = str_target, RPH = target)
    else:
        write_files(directory = str_target, PHHH = target)
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
