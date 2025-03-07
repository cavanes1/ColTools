#!/bin/bash
#SBATCH --job-name=LST
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 72:0:0
set -e
date
module list
python lst.py
date
sacct --name=LST --format="JobID,JobName,Elapsed,State"
