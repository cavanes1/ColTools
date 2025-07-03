\# ThiiraneStretcher

This code is similar to PhosphineStretcher, but is used to study thiirane, also known as ethylene sulfide, instead of phosphine (PH3).



This respository is used to run calculations of thiirane geometries where the S-CC distance is altered from equilibrium.

It can run an initial point with SCF and MCSCF, and then run adjacent points using the orbitals of the previous point as a starting point.

It can also run SCF at each geometry before MCSCF.

The default key inputs are for an active space of 12 DOCC + 6 CAS (orbitals).

