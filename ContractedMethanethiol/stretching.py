# parameters
ID = "CM"
coordinate = "CS"
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
file = "geom"
# bond lengths in Angstroms
CS = 1.797
SH = 1.331
CH1 = 1.085
CH2 = 1.087
# angles in degrees
CSH = 95.1
SCH1 = 109.9
SCH23 = 129.3
H2CH3 = 108.0

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
    f = open(directory + '.xyz', "w")
    f.write("  6\n")
    f.write("methanethiol\n")
    f.write("S       " + RCS + zero + zero + "\n")
    f.write("C       " + zero + zero + zero + "\n")
    f.write("H       " + Hx + Hy + zero + "\n")
    f.write("H       " + H1x + H1y + zero + "\n")
    f.write("H       " + H2x + H2y + H2z + "\n")
    f.write("H       " + H2x + H2y + H3z + "\n")
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
S=vtz
C=vtz
H=vtz
end

geomtyp=xyz
noorient
symmetry,nosym

bohr
geometry={name}.xyz

{{rhf;closed,13;wf,26,1,0}}
{{multi;occ,17;closed,8;wf,26,1,0;state,3;maxit,40}}

{{ci;occ,17;closed,8;core,1;wf,26,1,0;state,3;save,4001.1;expec,dm;maxiter,100,100}}
show,trdmx,trdmy,trdmz""".format(name=directory))
    h.close()

# this function runs the python script in SLURM
def slurmcop(target):
    str_target = format(target, ".2f")
    # produce the correct geom and slurm files
    if coordinate == "CS":
        write_files(directory = str_target, RCS = target)
    else:
        write_files(directory = str_target, RSH = target)
    # run Columbus interactivelyish
    rv = subprocess.run(["sbatch", str_target + ".sh"],cwd="./",capture_output=True)
    print(rv.stdout.decode('utf8'))

# run copyfunction automatically
right = np.arange(leftmost, rightmost + 0.001, step)
for gm in right:
    slurmcop(gm)
