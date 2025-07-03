# PhosphineStretcher

This code is similar to MethanethiolStretcher, but is used to study phosphine (PH3) instead of methanethiol (CH3SH).

This code is not receiving updates for the time being due to difficulties in calculation caused by interference between Rydberg and d orbitals mixing with antibonding orbitals.



This respository is used to run calculations of phosphine geometries where either the P-H bond or the PH-HH distance is altered from equilibrium.

It can run an initial point with SCF and MCSCF, and then run adjacent points using the orbitals of the previous point as a starting point.

It can also run SCF at each geometry before MCSCF.

The default key inputs are for an active space of 5 DOCC + 9 CAS (orbitals).

The default key inputs for MRCI are for an active space of 5 CORE + 9 ACT (orbitals).

The optimal basis set was being explored and was thought to possibly be a variation of cc-pVTZ for P and cc-pVDZ for H.

