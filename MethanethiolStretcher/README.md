\# MethanethiolStretcher

This code is similar to IterativeStretcher, but is used to study methanethiol (CH3SH) instead of methyl radical (CH3).

This code is no longer receiving updates for the time being because the molecule is not conducive to the type of calculations that are desired.



This respository is used to run calculations of methanethiol geometries where either the C-S or the S-H bond is altered from equilibrium.

It can run an initial point with SCF and MCSCF, and then run adjacent points using the orbitals of the previous point as a starting point.

It can also run SCF at each geometry before MCSCF.

The default key inputs are for an active space of 6 DOCC + 7 RAS + 0 CAS + 3 AUX (orbitals).

The default key inputs for MRCI are for an active space of 6 CORE + 7 ACT + 3 AUX (orbitals).

