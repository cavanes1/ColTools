#!/bin/bash
#SBATCH --job-name=jobname
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -c 1
#SBATCH -t 72:0:0
set -e
date
module list
python stretching.py
date
sacct --name=jobname --format="JobID,JobName,Elapsed,State"
