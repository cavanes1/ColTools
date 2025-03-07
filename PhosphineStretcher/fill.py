# module imports
import os
import subprocess

# make list of bond length distances
path = './'
distances = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]

for distance in distances:
    # for points to the right
    script_name = distance + "R.sh"
    f = open(script_name, "w")
    f.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p shared
#SBATCH -c 1
#SBATCH -t 72:0:0
set -e
date
ml python/3.7
module list
python stretching.py {dis}
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=distance+"R",dis=distance))
    f.close()
    rv = subprocess.run(["sbatch", script_name],cwd="./",capture_output=True)
    print(rv.stdout.decode('utf8'))
    
    # for points to the left
    script_name = distance + "L.sh"
    g = open(script_name, "w")
    g.write("""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --account=dyarkon1
#SBATCH -p shared
#SBATCH -c 1
#SBATCH -t 72:0:0
set -e
date
ml python/3.7
module list
python lstretching.py {dis}
sacct --name={name} --format="JobID,JobName,Elapsed,State"
date""".format(name=distance+"L",dis=distance))
    g.close()
    rv = subprocess.run(["sbatch", script_name],cwd="./",capture_output=True)
    print(rv.stdout.decode('utf8'))