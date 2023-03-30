# parameters
drti = 1
drtf = 1
statei = 1
statef = 1
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

# read from polyhesls
f = open(direc + "/LISTINGS/polyhesls.all", "r")
lines = f.readlines()
f.close()
print("Data read from polyhesls")

# extract data from Cartesian geometry to obtain its structure
f = open(direc + "/geom", "r")
cart = f.readlines()
f.close()
cart_data = []
for line in cart:
    cart_data.append(line.split())
print("Cartesian geometry structure data extracted")
