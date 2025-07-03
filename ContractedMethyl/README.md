# ContractedMethyl

This code is no longer receiving updates for the time being because the author is shifting their focus to a different molecule.



This respository is used to run calculations on Molpro of methyl radical (CH3) geometries where a C-H bond is altered from equilibrium.

It runs points simultaneously with SCF, MCSCF, and internally contracted MRCI.



## Workflow

1. Make a directory

2. Upload the python files to the directory

3. Edit stretching.py with the desired settings such as ID and geometry distortion

  - If not doing MRCI, change partition to shared, change core allocation (including removing -t 24), and remove CI instructions

4. Run stretching.py to submit jobs to SLURM

5. Extract energies by running ee.py

  - Change CI variable from True if not doing MRCI

6. View surfaces using Jupyter notebook

