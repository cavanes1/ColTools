# parameters
drti = 1
drtf = 1
statei = 1
statef = 2
r = 0.1 # radius of loop in units of g/h - Bohr?
step = 1 # Step size/pi in radians
direc = "12CI" # x and y vectors are obtained using this
choseniter = 54 # choice code, NOT iteration!

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# the following code blocks extract the x and y vectors
# read from polyhesls
f = open(direc + "/LISTINGS/polyhesls.all", "r")
lines = f.readlines()
f.close()
print("Data read from polyhesls")

# extract data from polyhesls
position = 0
iteration = 0
read_geom = False
cartzone = False
read_g = False
read_h = False
data = []
for line in lines:
    if "iteration" in line:
        iteration = int(line.split()[3])
        data.append([iteration,[],[],[]])
    if line == "\n":
        read_geom = False
        read_h = False
    if read_geom:
        data[-1][1].append(line.split())
    if "GEOMETRY" in line:
        read_geom = True
    if "cartesian" in line:
        cartzone = True
    if "internal" in line:
        cartzone = False
        read_g = False
    if cartzone:
        if "HR=" in line:
            read_h = True
        if "GR=" in line:
            read_g = True
        if read_h:
            data[-1][3].append(line.split()[-3:])
        if read_g:
            data[-1][2].append(line.split()[-3:])
print("Data extracted from polyhesls")

# select polyhesls iteration to use
print("List of iterations:")
for iteration in range(len(data)):
    print("Choice " + str(iteration) + ": "  + str(data[iteration][0]))
print("Using iteration choice code: " + str(choseniter))
cdata = data[int(choseniter)]

# create x and y vectors
g = []
for triplet in cdata[2]:
    for entry in triplet:
        g.append(float(entry[:-1]))
g = np.array(g)
print("\ng vector")
print(g)
h = []
for triplet in cdata[3]:
    for entry in triplet:
        h.append(float(entry[:-1]))
h = np.array(h)
print("\nh vector")
print(h)
x = g/np.linalg.norm(g)
print("\nx vector (normalized g)")
print(x)
y = h/np.linalg.norm(h)
print("\ny vector (normalized h)")
print(y)
print("Orthogonal intersection adapted coordinate unit vectors created")

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
count = 1
for dercp in nadvecs:
    updated = dercp
    print("\nRaw f:")
    print(dercp)
    flip = input("\n" + str(count) + " - Multiply derivative coupling by (enter 1 or -1): ")
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
    count += 1
print("\nCorrected cartgrd.nad data together:")
print(corrected_nadvecs)

# calculate dot products
integral = 0
count = 0
for direc in direcs:
    # generate dR unit vector
    target = int(direc)
    theta = step*target*np.pi
    print("\nTheta = " + str(theta))
    theta2 = theta + (np.pi/2)
    dRunit = np.cos(theta2)*x + np.sin(theta2)*y
    #print(dRunit)
    # check for unity
    #print("Norm of dR = " + str(np.linalg.norm(dRunit)))
    # obtain f vector
    f = corrected_nadvecs[count]
    #print(f)
    # dot multiplication
    dot = np.vdot(f, dRunit)
    print("Dot product = " + str(dot))
    # integrate via summation
    integral += dot
    count += 1

# produce final result
integral *= np.pi*r*step
print("\nLoop integral = " + str(integral))
