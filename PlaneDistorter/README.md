# PlaneDistorter

This code is similar to IterativeStretcher, but involves a different set of geometries.

This code will soon be modified to an upgraded supercomputer system.

This code is no longer receiving updates for the time being because the author is shifting their focus to a different molecule.

The default key inputs are for an active space of 1 DOCC (CORE for MRCI) + 10 CAS (orbitals).



This respository is used to run calculations of methyl radical (CH3) geometries where the carbon atom is moved perpendicular from the hydrogen-containing plane.

It runs an initial point with SCF and MCSCF, and then runs adjacent points using the orbitals of the previous point as a starting point.

