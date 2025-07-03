\# TetrazolylTools

This is a group of codes that I have used in my research on the tetrazolyl neutral radical.



\## Exclusives

These tools are only in this directory and have not been generalized to all molecules



\### surfcurve.py

Given two points, this generates geom.all with linear synchronous transit points and calculates a curve plot using dat.x.



\### stretching.py

This moves a single atom along a single Cartesian unit vector.



\### vec.py

Generates geometries in the direction of a given Cartesian vector.

Other required inputs are step size (in units of multiples of the given vector) and number of steps, as well as the directory containing the initial geometry.

The initial geometry directory gets copied to new directories, each one having its geometry replaced by a generated point.

A job is then submitted for each of the generated directories.



\### Geometry rippers



\* angxyz.py: Converts one COLUMBUS geometry file into .xyz format.

\* allangxyz.py: Does this for all geometries in a GEOMS directory.

\* ghripper.py: Generates .xyz files with vectors included, one for each conical intersection search iteration of a polyhes listings file.



\## Key inputs



\### makscfky

This is the SCF key input. It describes 17 doubly-occupied orbitals and one open shell orbital.



\### makmcky

This is the MCSCF key input. It describes 11 doubly-occupied orbitals and 9 complete active space orbitals.



\### cidrtplky

This is the MRCI key input. It describes 5 frozen core orbitals, 6 doubly-occupied orbitals, and 9 complete active space orbitals.



\### pscript.sh

This is a good parallel SLURM script input starting point. It is designed to run on the Rockfish cluster of ARCH.



\## intcfl

C2v-symmetrized internal coordinate scheme.

Only the first 5 coordinates are nonzero in C2v symmetry.

