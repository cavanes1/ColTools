# ColTools
This is a set of codes that work for any molecule while using COLUMBUS.

## Curve plots

### extractenergies.py
Extracts MCSCF energies and number of iterations to convergence from each subdirectory of the current directory.

### CIEE.py
Extracts MRCI energies and number of iterations to convergence from each subdirectory of the current directory.

### MCSCF.ipynb
Example Jupyter notebook that generates a potential energy curve from extracted energy file.

## Conical intersection search

### enerview.py
Prints information from energy.all in a format that is easier to interpret. Energy differences are shown in wavenumbers.

### 2low.py
Searches for the lowest energy CI search iteration for each subdirectory and compares by energy while providing additional information.

### conview.py
Generates Python lists of data about the right-hand-side norm of the Newton-Raphson equation.

## Linear synchronous transit
Generates a linear path between two geometries in internal coordinates (specifically, those automatically generated by intc.x).

### lst.py
Performs linear synchronous transit one point at a time, carrying over the previous MCSCF molecular orbital coefficients to each subsequent geometry.
Requires script.sh to launch

### simul.py
Performs linear synchronous transit by calculating all points of the path simultaneously.

### runcol.py
Resubmits jobs for all directories using the settings of a single directory. One can expect to use this to run MRCI after having used lst.py to run MCSCF.

## Line integral test
Performs a circular loop integral of the derivative coupling.
The code is divided into two parts, linA.py and linB.py.
linA.py generates the points and runs jobs for them, whereas linB.py extracts and analyzes the resulting data after the calculations complete.

### linA.py
Only the directory with the conical intersection search is required (and also linA.py). However, it is important to perform COLUMBUS input for nadcoupl.
Molecular orbital coefficients are grabbed from MOCOEF/mocoef_mc.sp, so if a single point calculation was not performed with the directory, it may be a good idea to place the coefficients as "mocoef" directly in the directory and then comment out this part of the code.

### linB.py
A value of pi indicates a conical intersection (or an odd number in the loop) whereas a value of zero indicates a lack thereof (or an even number).
16 points should give 3.14, 8 points should give 3.

## Geometry analysis

### geomprint.py
Prints the geometry of a point in Cartesian and intc.x-generated internal coordinates in Python list format.

### dist.py
This tool calculates the distance between two given geometries in three ways:
1. Cartesian distance of raw input geometry files
2. Cartesian distance such that the second geometry is moved to match the relative position of the first
3. Internal coordinate distance (using scheme generated by intc.x)
   - Also provides the normalized internal coordinate vector between the geometries

All distances are the 2-norm.

### point line distance.ipynb
Calculates the shortest distance in 2-norm between a point from the line generated from two other points.
Also yields the point on the line closest to the given point not on the line.

## gradcomp.py
Compares gradients and nonadiabatic couplings between two ab initio calculated points.

## geomkick.py
Takes an input file of internal coordinates and makes copies of a chosen directory with the geometry replaced with those in the input file.
The last line of the input file must be "END".

## Surfgen tools

### surfextractor.pl
Extracts the necessary data for Surfgen.

### points.py
Identifies quasidegeneracies from energy.all to generate points.in.
Designed with SurfgenBound 2023 in mind.
