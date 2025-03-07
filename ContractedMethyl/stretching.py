# parameters
ID = "CM"
leftmost = 1
rightmost = 7
step = 0.1 # spacing

# module imports
import numpy as np
import os
import subprocess
import sys
print("all modules imported")

# delete .git directory
#os.system("rm -rf .git")
#print(".git directory deleted")

# physical constants
equilibrium_BD = 1.079 # angstroms
conversion_factor = 1.889726125 # Bohr radii per angstrom
converted_EBD = equilibrium_BD*conversion_factor
zero = format(0, "14.8f")
neg_half = format(-0.5*converted_EBD, "14.8f")
square_root = 0.86602540378443864676 # sqrt(3)/2
pos_y = format(square_root*converted_EBD, "14.8f")
neg_y = format(-1*square_root*converted_EBD, "14.8f")
# distorted
Dneg_y = format(-1.69, "14.8f")
Dzero = format(0.5, "14.8f")
print("physical constants prepared")

# for a single geometry
def write_files(directory = 'equil', stretch = converted_EBD):
    stretch = format(stretch, "14.8f")

    # write geometry file
    f = open(directory + '.xyz', "w")
    f.write("  4\n")
    f.write("methyl radical\n")
    f.write("C       " + zero + zero + zero + "\n")
    f.write("H       " + neg_half + pos_y + zero + "\n")
    f.write("H       " + neg_half + neg_y + zero + "\n")
    f.write("H       " + stretch + zero + zero + "\n")
    f.close()

    # write SLURM file
    g = open(directory + '.sh', "w")
    g.write("""#!/bin/bash -l

#SBATCH --job-name={jobname}
#SBATCH --account=dyarkon1
#SBATCH -p parallel
#SBATCH -N 1
#SBATCH -t 10:0:0
#SBATCH -c 24

module list
$MOLPRO/molpro --no-xml-output -d /dev/shm/ -t 24 {name}.com
sacct --name={jobname} --format="JobID,JobName,Elapsed,State"
date""".format(name=directory, jobname=ID+directory))
    g.close()

    # write job file
    h = open(directory + '.com', "w")
    # Note: Input may be wrong
    h.write("""***, CH3
memory,1000,m

basis
C=avtz
H=avtz
end

geomtyp=xyz
noorient
symmetry,nosym

bohr
geometry={name}.xyz

{{rhf;closed,4;open,1.1;wf,9,1,1}}
{{multi;occ,11;closed,1;wf,9,1,1;state,6;maxit,40}}

{{ci;occ,11;closed,1;core,1;wf,9,1,1;state,6;save,4001.1;expec,dm;maxiter,100,100}}
show,trdmx,trdmy,trdmz""".format(name=directory))
    h.close()

# this function runs the python script in SLURM
def slurmcop(target):
    str_target = format(target, ".2f")
    # produce the correct geom and slurm files
    write_files(str_target, target)
    # run Columbus interactivelyish
    rv = subprocess.run(["sbatch", str_target + ".sh"],cwd="./",capture_output=True)
    print(rv.stdout.decode('utf8'))

# run copyfunction automatically
right = np.arange(leftmost, rightmost + 0.001, step)
for gm in right:
    slurmcop(gm)
