#!/bin/bash
#SBATCH --job-name=NY
#SBATCH --account=dyarkon1
#SBATCH -p defq
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -t 72:0:0
set -e
module list
$COLUMBUS/runc -m 160000 -nproc 48 > runls
cp WORK/ciudg.perf .
rm -r WORK
sacct --name=NY --format="JobID,JobName,Elapsed,State"
date
