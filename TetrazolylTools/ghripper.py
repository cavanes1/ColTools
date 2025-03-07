# module import
import numpy as np
import os

# read from polyhesls
allfiles = os.listdir("GEOMS")
f = open("LISTINGS/polyhesls.all", "r")
lines = f.readlines()
f.close()

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
            data[-1][3].append([float(line.split()[-3][:-1]), float(line.split()[-2][:-1]), float(line.split()[-1][:-1])])
        if read_g:
            data[-1][2].append([float(line.split()[-3][:-1]), float(line.split()[-2][:-1]), float(line.split()[-1][:-1])])

def writecartesian(geomdata, vecdata):
    conversion = 0.529177211
    xstr = format(float(geomdata[1])*conversion, "13.6f")
    ystr = format(float(geomdata[2])*conversion, "13.6f")
    zstr = format(float(geomdata[3])*conversion, "13.6f")
    xvec = format(vecdata[0]*conversion, "13.6f")
    yvec = format(vecdata[1]*conversion, "13.6f")
    zvec = format(vecdata[2]*conversion, "13.6f")
    return xstr + ystr + zstr + xvec + yvec + zvec

def filewrite(filename, geomdata, vecdata):
    g = open("GEOMS/" + filename + ".xyz", "w")

    # write to file
    g.write("6\n\n")
    g.write(" N  " + writecartesian(geomdata[0], vecdata[0]) + "\n")
    g.write(" N  " + writecartesian(geomdata[1], vecdata[1]) + "\n")
    g.write(" N  " + writecartesian(geomdata[2], vecdata[2]) + "\n")
    g.write(" N  " + writecartesian(geomdata[3], vecdata[3]) + "\n")
    g.write(" C  " + writecartesian(geomdata[4], vecdata[4]) + "\n")
    g.write(" H  " + writecartesian(geomdata[5], vecdata[5]) + "\n")
    g.close()

# print data
for datum in data:
    print("Generating files for iteration " + str(datum[0]))
    # take the Frobenius norm of each g and h vector (units are still a0 here)
    ng = np.array(datum[2])/np.linalg.norm(datum[2])
    nh = np.array(datum[3])/np.linalg.norm(datum[3])
    print("g norm = " + str(np.linalg.norm(datum[2])) + " a0")
    print("h norm = " + str(np.linalg.norm(datum[3])) + " a0")

    # write files
    filewrite("g" + str(datum[0]), datum[1], ng)
    filewrite("h" + str(datum[0]), datum[1], nh)
