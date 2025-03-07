# run slurmcop? and parameters
coordinate = "CS"
autocop = 'r'
leftmost = 2.5
rightmost = 7
start = 3.4 # initial geometry
# CS is 3.40 Bohr and SH is 2.52 Bohr
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
CS = 1.85908
SH = 1.35167
CH1 = 1.08334
CH2 = 1.08254
# angles in degrees
CSH = 96.40321
SCH1 = 106.06354
SCH23 = 127.65858
H2CH3 = 110.97987

# converting to Bohr radii and radians
conversion_factor = 1.889726125 # Bohr radii per angstrom
CS *= conversion_factor
SH *= conversion_factor
CH1 *= conversion_factor
CH2 *= conversion_factor
CSH *= np.pi/180
SCH1 *= np.pi/180
SCH23 *= np.pi/180
H2CH3 *= np.pi/180
CH23 = CH2*np.cos(H2CH3/2)
# equilibrium coordinates
H1x = -1*CH1*np.cos(np.pi-SCH1)
H1y = CH1*np.sin(np.pi-SCH1)
H2x = -1*CH23*np.cos(np.pi-SCH23)
H2y = -1*CH23*np.sin(np.pi-SCH23)
H2z = CH2*np.sin(H2CH3/2)
H3z = -1*H2z
# formatting numbers
zero = format(0, "14.8f")
H1x = format(H1x, "14.8f")
H1y = format(H1y, "14.8f")
H2x = format(H2x, "14.8f")
H2y = format(H2y, "14.8f")
H2z = format(H2z, "14.8f")
H3z = format(H3z, "14.8f")
print("physical constants prepared")

# for a single geometry
def write_files(directory = 'equil', RCS = CS, RSH = SH):
    Hx = format(RSH*np.cos(np.pi-CSH) + RCS, "14.8f")
    Hy = format(-1*RSH*np.sin(np.pi-CSH), "14.8f")
    RCS = format(RCS, "14.8f")
    # write geometry file (Hydrogen order is H, H1, H2, H3)
    f = open(directory + '/' + file, "w")
    f.write(" S    16.0" + RCS + zero + zero + "   31.97207117\n")
    f.write(" C     6.0" + zero + zero + zero + "   12.00000000\n")
    f.write(" H     1.0" + Hx + Hy + zero + "    1.00782504\n")
    f.write(" H     1.0" + H1x + H1y + zero + "    1.00782504\n")
    f.write(" H     1.0" + H2x + H2y + H2z + "    1.00782504\n")
    f.write(" H     1.0" + H2x + H2y + H3z + "    1.00782504\n")
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
    else:
        write_files(directory = str_target, RSH = target)
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
