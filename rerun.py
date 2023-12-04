# resubmit failed jobs
resubmit = True
clnup = False # if true this only kills jobs and does not restart them

# module imports
import time
import numpy as np
import subprocess
import os
print("all modules imported")

# make list of bond length distances
path = './'
alldistances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
alldistances.remove("ORIGIN")

if resubmit:
    for distance in alldistances:
        allfls = os.listdir("./" + distance)
        if "runc.error" not in allfls:
            print(distance + " is pending")
            continue
        f = open("./" + distance + "/runc.error", "r")
        lines = f.readlines()
        f.close()
        killjob = False
        for line in lines:
            if "ierr" in line:
                killjob = True
                break
        if killjob:
            print(distance + " needs to be killed and restarted")
            allfls = os.listdir("./" + distance)
            for fl in allfls:
                if "slurm-" in fl:
                    SLURMid = fl.split("-")[1].split(".")[0]
                    os.system("scancel " + SLURMid)
                    if not clnup:
                        time.sleep(5)
                    os.system("rm ./" + distance + "/"  + fl)
            if not clnup:
                os.system("rm ./" + distance + "/runc.error")
                rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+distance,capture_output=True)
                print(rv.stdout.decode('utf8'))
        else:
            print(distance + " is OK")

else:
    for distance in alldistances:
        print(distance)
        rv = subprocess.run(["sbatch", "script.sh"],cwd="./"+distance,capture_output=True)
        print(rv.stdout.decode('utf8'))
