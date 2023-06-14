# parameters
dir1 = "../FLIPSYM3" # location of first directory
dir2 = "." # location of second directory
stct = 5 # number of electronic states
print("Comparing directories " + dir1 + " and " + dir2 + " for " + str(stct) + " states.")

# module import
import numpy as np
import os
import subprocess
print("Modules imported.")

# main routine
def gradcomp(statei, statef, drti = 1, drtf = 1):
    # determine name of files
    filename = "intgrd."
    # if not a gradient
    if not statei == statef:
        filename += "nad."
    filename += "drt" + str(drti) + ".state" + str(statei)
    if not statei == statef:
        filename += ".drt" + str(drtf) + ".state" + str(statef)
    filename += ".sp"
    # extract data from files
    f = open(dir1 + "/GRADIENTS/" + filename, "r")
    gradraw1 = f.readlines()
    f.close()
    f = open(dir2 + "/GRADIENTS/" + filename, "r")
    gradraw2 = f.readlines()
    f.close()
    grad1 = []
    grad2 = []
    for i in gradraw1:
        if i[0:3] == "***":
            grad1.append(float("nan"))
        else:
            grad1.append(float(i))
    for i in gradraw2:
        if i[0:3] == "***":
            grad2.append(float("nan"))
        else:
            grad2.append(float(i))
    grad1 = np.array(grad1)
    grad2 = np.array(grad2)
    # compare gradients
    return grad2/grad1

# function that prints results of the comparison
def coordprint(statei, statef):
    comp = gradcomp(statei, statef)
    for j in range(len(comp)):
        if comp[j] < -1.05 or comp[j] > 1.05:
            flag = "   !!!"
        elif comp[j] > -0.95 and comp[j] < 0.95:
            flag = "   !!!"
        else:
            flag = ""
        print("   Coordinate " + format(j + 1, "2.0f") + ": " + format(comp[j], "8.4f") + flag)

# gradients
print("\nGradients")
for i in range(1, stct + 1):
    print("\nState " + str(i) + ":")
    coordprint(i, i)

# nonadiabatic couplings
print("\n\n\nNonadiabatic couplings")
for i in range(1, stct + 1):
    for j in range(i + 1, stct + 1):
        print("\nStates " + str(i) + " and " + str(j) + ":")
        coordprint(i, j)
