# parameters
drti = 1
drtf = 1
statei = 1
statef = 2
r = 0.1 # radius of loop in units of g/h - Bohr?
step = 1 # Step size/pi in radians

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# generate list of expected directories
direcs = []
for i in range(int(2/step)):
    direcs.append(str(i + 1))

# read derivative couplings
nadvecs = []
for direc in direcs:
    f = open(direc + "/GRADIENTS/cartgrd.nad.drt" + str(drti) + ".state" + str(statei)
            + ".drt" + str(drtf) + ".state" + str(statef) + ".sp", "r")
    nad = f.readlines()
    f.close()
    nadvec = []
    for triplet in nad:
        for entry in triplet.split():
            nadvec.append(float(entry))
    nadvec = np.array(nadvec)
    print("\ncartgrd.nad data from directory " + direc + ":")
    print(nadvec)
    nadvecs.append(nadvec)
print("\nAll cartgrd.nad data together:")
print(nadvecs)

# input sign flips
corrected_nadvecs = []
for dercp in nadvecs:
    updated = dercp
    print("\nRaw f:")
    print(dercp)
    flip = input("\nMultiply derivative coupling by (enter 1 or -1): ")
    if flip == "1":
        print("Leaving unchanged")
    elif flip == "-1":
        print("Flipping sign")
        updated *= -1
    else:
        print("Leaving unchanged")
    print("\nUpdated f:")
    print(updated)
    corrected_nadvecs.append(updated)
print("\nCorrected cartgrd.nad data together:")
print(corrected_nadvecs)

# calculate dot products
count = 0
for direc in direcs:
    # generate dR unit vector
    target = int(direc)
    theta = step*target*np.pi
    print("Theta = " + str(theta))
    theta2 = theta + (np.pi/2)
    dRunit = np.cos(theta2)*x + np.sin(theta2)*y
    # obtain f vector
    f = corrected_nadvecs[count]
    # dot multiplication

# integrate via summation
