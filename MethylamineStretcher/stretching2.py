# run slurmcop? and parameters
autocop = 'r'
leftmost = 1
rightmost = 8
start = 2.8 # initial geometry
step = 0.1 # spacing

# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# physical constants
file = "geom"
# bond lengths in Angstroms
CN = 1.474
NH = 1.011
CH = 1.093
# angles in degrees
CNH = 112
NCH1 = 109.9
NCH23 = 129.3
H2CH3 = 109.5
HNH = 105.5

# converting to Bohr radii and radians
conversion_factor = 1.889726125 # Bohr radii per angstrom
CN *= conversion_factor
NH *= conversion_factor
CH *= conversion_factor
CNH *= np.pi/180
NCH1 *= np.pi/180
NCH23 *= np.pi/180
H2CH3 *= np.pi/180
HNH *= np.pi/180
CH23 = CH*np.cos(H2CH3/2)
NH45 = NH*np.cos(HNH/2)
# equilibrium coordinates
# from methanethiol
H1x = -1*CH*np.cos(np.pi-NCH1)
H1y = CH*np.sin(np.pi-NCH1)
H2x = -1*CH23*np.cos(np.pi-NCH23)
H2y = -1*CH23*np.sin(np.pi-NCH23)
H2z = CH*np.sin(H2CH3/2)
H3z = -1*H2z
# new atoms
H45y = NH45*np.sin(np.pi-NCH23) # reuse angle
H4z = NH*np.sin(HNH/2)
H5z = -1*H4z
# formatting numbers
zero = format(0, "14.8f")
H1x = format(H1x, "14.8f")
H1y = format(H1y, "14.8f")
H2x = format(H2x, "14.8f")
H2y = format(H2y, "14.8f")
H2z = format(H2z, "14.8f")
H3z = format(H3z, "14.8f")
H45y = format(H45y, "14.8f")
H4z = format(H4z, "14.8f")
H5z = format(H5z, "14.8f")
print("physical constants prepared")

# for a single geometry
def write_files(directory = 'equil', RCN = CN):
    H45x = format(NH45*np.cos(np.pi-NCH23) + RCN, "14.8f") # reuse angle
    RCN = format(RCN, "14.8f")
    # write geometry file (Hydrogen order is H, H1, H2, H3)
    f = open(directory + '/' + file, "w")
    f.write(" N     7.0" + RCN + zero + zero + "   14.00307400\n")
    f.write(" C     6.0" + zero + zero + zero + "   12.00000000\n")
    f.write(" H     1.0" + H1x + H1y + zero + "    1.00782504\n")
    f.write(" H     1.0" + H2x + H2y + H2z + "    1.00782504\n")
    f.write(" H     1.0" + H2x + H2y + H3z + "    1.00782504\n")
    f.write(" H     1.0" + H45x + H45y + H4z + "    1.00782504\n")
    f.write(" H     1.0" + H45x + H45y + H5z + "    1.00782504\n")
    f.close()
    # write SLURM file
    g = open(directory + '/script.sh', "w")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -c 1
#SBATCH -t 72:0:0
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
    write_files(directory = str_target, RCN = target)
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
    write_files(directory = str_target, RCN = target)
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
