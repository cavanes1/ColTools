#!/bin/bash
#SBATCH --job-name=jobname
#SBATCH --account=dyarkon1
#SBATCH -p shared
#SBATCH -c 1
#SBATCH -t 72:0:0
set -e
date
ml python/3.7
module list
python distort.py
date
sacct --name=jobname --format="JobID,JobName,Elapsed,State"
