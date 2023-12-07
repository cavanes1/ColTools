# run this program in a directory where
# COLUMBUS has been run in many subdirectories for various geometries

fill = False

# module imports
import numpy as np
import subprocess
import os
print("all modules imported")

# make list of bond length distances
path = './'
distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
print("finished producing distance list")
if '.git' in distances:
    distances.remove('.git')
    print(".git directory detected and ignored")

def clean():
    os.system("mkdir MOS")
    os.system("mkdir MOC")
    # delete WORK and old subdirectories in each geometry's directory
    for distance in distances:
        os.system("cp " + distance + "/WORK/ciudg.perf " + distance) # only for parallel
        os.system("rm -r " + distance + "/WORK")
        os.system("rm -r " + distance + "/old") # no longer in use
        print("Finished cleanup of " + distance)
        # consolidate MOLDEN outputs and mocoefs
        os.system("cp " + distance + "/MOLDEN/molden_mo_mc.sp MOS/" + distance)
        os.system("cp " + distance + "/MOCOEFS/mocoef_mc.sp MOC/" + distance)
    # remove old slurm output(s)
    if fill:
        flist = [file for file in os.listdir(path) if os.path.isfile(path+file)]
        print("file list generated")
        os.system("mkdir SLURM")
        os.system("mkdir SH")
        for file in flist:
            if 'slurm' in file:
                os.system("mv " + path + file + " " + path + "SLURM")
                print("moved " + file)
            if '.sh' in file:
                os.system("mv " + path + file + " " + path + "SH")
                print("moved " + file)

# run function
clean()
print("all done!")
