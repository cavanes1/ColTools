ID = ""
SD = "0" # colinp'ed directory
parallel = True
immediate = True

# module imports
import numpy as np
import subprocess
import os
print("all modules imported")

# make list of bond length distances
path = './'
alldistances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
print("finished producing distance list")
if '.git' in alldistances:
    alldistances.remove('.git')
    print(".git directory detected and ignored")

# SLURM script
sscript = ""
if not parallel:
    sscript = """#!/bin/bash
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
date"""
else:
    sscript = """#!/bin/bash
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
date"""

# run Columbus at each geometry
distances = alldistances.copy()
distances.remove(SD)
def runcol():
    for distance in distances:
        # rename old directory
        os.system("mv " + distance + " temporary")
        # copy SD
        os.system("cp -rv " + SD + " " + distance)
        # remove old files
        os.system("rm " + distance + "/geom")
        os.system("rm " + distance + "/script.sh")
        os.system("rm " + distance + "/mocoef")
        # add correct files
        os.system("cp temporary/geom " + distance)
        g = open(distance + '/script.sh', "w")
        g.write(sscript.format(name=distance+ID))
        g.close()
        os.system("cp temporary/MOCOEFS/mocoef_mc.sp " + distance + "/mocoef")
        # delete temporary directory
        os.system("rm -rv temporary")
        print(distance + " is prepared\n")
    # for SD
    os.system("rm " + SD + "/mocoef")
    os.system("cp " + SD + "/MOCOEFS/mocoef_mc.sp " + SD + "/mocoef")
    g = open(SD + '/script.sh', "w")
    g.write(sscript.format(name=SD+ID))
    g.close()
    print(SD + " is prepared\n")
    # run Columbus
    # immediate job submission
    if immediate:
        for distance in alldistances:
            rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+distance,capture_output=True)
            print(rv.stdout.decode('utf8'))

# run function
runcol()
print("all done!")
