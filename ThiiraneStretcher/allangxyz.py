# module import
import numpy as np
import os

# list of files in GEOMS
allfiles = os.listdir("GEOMS")
print(allfiles)
selectedfiles = []
for file in allfiles:
    if ".xyz" not in file and "int" not in file and "disp" not in file:
        selectedfiles.append(file)
print(selectedfiles)
for file in selectedfiles:
    print("Working on " + file)
    # extract data
    f = open("GEOMS/" + file, "r")
    lines = f.readlines()
    f.close()

    # extract coordinates
    oldgeom = []
    for i in lines:
        temporary_list = i.split()[2:5]
        temporary_list = [float(i) for i in temporary_list]
        oldgeom.append(temporary_list)
    oldgeom = np.array(oldgeom)
    print("Old geometry")
    print(oldgeom)

    # overwrite geom
    g = open("GEOMS/" + file + ".xyz", "w")

    def writecartesian(arr):
        xstr = format(arr[0]*0.529177211, "13.6f")
        ystr = format(arr[1]*0.529177211, "13.6f")
        zstr = format(arr[2]*0.529177211, "13.6f")
        return xstr + ystr + zstr

    # write to file
    g.write("4\n\n")
    g.write(" P  " + writecartesian(oldgeom[0]) + "\n")
    g.write(" H  " + writecartesian(oldgeom[1]) + "\n")
    g.write(" H  " + writecartesian(oldgeom[2]) + "\n")
    g.write(" H  " + writecartesian(oldgeom[3]) + "\n")
    g.close()
