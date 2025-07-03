# IterativeStretcher

This code replaces StretchExtractor.

This code is no longer receiving updates for the time being because the author is shifting their focus to a different molecule due to feasibility issues caused by the large number of required states.

The default key inputs are for an active space of 1 DOCC (CORE for MRCI) + 10 CAS (orbitals).



This respository is used to run calculations of methyl radical (CH3) geometries where a C-H bond is altered from equilibrium.

It can run an initial point with SCF and MCSCF, and then run adjacent points using the orbitals of the previous point as a starting point.

It can also run SCF at each geometry before MCSCF.

