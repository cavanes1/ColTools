# parameters
automatic = True
preserve = 3

# import modules
import numpy as np
from os import listdir
from os.path import isfile, join
import os

# read files
# existing names with old order
f = open("names.all", "r")
oldnamefile = f.readlines()
f.close()
# new order
if not automatic:
    f = open("names.new", "r")
    newnamefile = f.readlines()
    f.close()
# absolute energy errors
if automatic:
    f = open("errener.dat", "r")
    errfile = f.readlines()
    f.close()

# extract data
# old name list
oldnames = []
for line in oldnamefile:
    currdat = line.split()
    #oldnames.append([int(currdat[0]), currdat[-1]])
    oldnames.append(currdat[-1])
# new name list
newnames = []
if not automatic:
    for line in newnamefile:
        newnames.append(line.split()[-1])
# error name list
errnames = []
grnderrs = []
if automatic:
    #position = 1
    for line in errfile:
        currdat = line.split()
        #errnames.append([position, line.split()[-1]])
        errnames.append(currdat[-1])
        grnderrs.append(abs(float(currdat[0])))
        #position += 1
    if errnames == oldnames:
        print("errener.dat has same name order as names.all")
    else:
        print("Inconsistency between errener.dat and names.all")

# identify relevant files
mypath = "./"
allfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
grdfiles = []
for fl in allfiles:
    if "cartgrd." in fl:
        grdfiles.append(fl)
print(grdfiles)

# back up files
relfiles = grdfiles + ["energy.all", "geom.all"]
if automatic:
    relfiles = relfiles + ["names.all", "errener.dat"]
os.system("mkdir OLDDATA")
for fl in relfiles:
    os.system("mv " + fl + " OLDDATA")

# automatically create new list
if automatic:
    en1 = errnames[:preserve]
    en2 = errnames[preserve:]
    ge1 = grnderrs[:preserve]
    ge2 = grnderrs[preserve:]
    en3 = [x for _,x in sorted(zip(ge2,en2))]
    newnames = en1 + en3

# sort
for name in newnames:
    print(name)
    origpos = oldnames.index(name)
    for fl in grdfiles + ["geom.all"]:
        f = open("OLDDATA/" + fl, "r")
        startread = origpos*6
        writethis = f.readlines()[startread:startread + 6]
        #print(writethis)
        f.close()
        f = open(fl, "a")
        for wt in writethis:
            f.write(wt)
        f.close()
    f = open("OLDDATA/energy.all", "r")
    writethis = f.readlines()[origpos]
    f.close()
    f = open("energy.all", "a")
    f.write(writethis)
    f.close()
    if automatic:
        f = open("OLDDATA/errener.dat", "r")
        g = open("OLDDATA/names.all", "r")
        fwrite = f.readlines()[origpos]
        gwrite = g.readlines()[origpos]
        f.close()
        g.close()
        f = open("errener.dat", "a")
        g = open("names.all", "a")
        f.write(fwrite)
        g.write(gwrite)
        f.close()
        g.close()
