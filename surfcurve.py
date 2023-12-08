# parameters
step = 0.01 # Step size, 0.04 is not bad
init_name = "intc.1MSD" # Path of initial internal coordinate geometry file
final_name = "intc.C2vCI" # Name of final internal coordinate geometry file
refgrab = True # Generate refgrab from geom.all and fit.in
overwrite = False # Overwrite backups

# cartgrd write and energy.all write need to be edited for the molecule of interest
# Before running, make sure you have
#   intg1 and intg2
#   intcfl
#   basis.in
#   Hd.CheckPoint
#   dat.x
#   geom.all (if refgrab = True)
#   fit.in   (if refgrab = True)
#   refgeom  (if refgrab = False)
#   geom     (if refgrab = False) same as refgeom
# This program automatically generates the required files
#   energy.all
#   names.all
#   refgeom

# module import
import numpy as np
from os import listdir
from os.path import isfile, join
import os
import subprocess
print("Modules imported")

# generate reference geometry
mypath = "./"
allfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if refgrab:
    f = open("./geom", "w")
    g = open("./refgeom", "w")
    # read fit.in
    h = open("fit.in", "r")
    fitin = h.readlines()
    h.close()
    enfDiab = 0
    natoms = 0
    for param in fitin:
        if "enfDiab" in param:
            enfDiab = int(param.split()[-1][:-1])
        if "natoms" in param:
            natoms = int(param.split()[-1])
    print("enfDiab = " + str(enfDiab))
    print("natoms  = " + str(natoms))

    # read geom.all
    gfl = "geom.all"
    if "geom.all.old" in allfiles:
        gfl = "geom.all.old"
    j = open(gfl, "r")
    lines = j.readlines()
    j.close()
    ref = lines[(enfDiab - 1)*natoms:enfDiab*natoms]

    # write refgeom
    for refline in ref:
        f.write(refline)
        g.write(refline)
    f.close()
    g.close()
    print("Reference geometry written to geom and refgeom")

# back up files which will be appended
filelist = ["geoms.txt", "geom.all", "names.all", "energy.all"]
for fl in filelist:
    if fl in allfiles: # if file exists
        if fl + ".old" not in allfiles: # if backup does not exist
            os.system("mv " + fl + " " + fl + ".old")
        elif overwrite: # if backup exists but I want to overwrite backups
            os.system("mv " + fl + " " + fl + ".old")
        else: # if backup exists but I do not want to overwrite backups
            os.system("rm " + fl)
print("Backup complete for files to be appended")

# read given internal coordinate geometry files
f = open(init_name, "r")
init = f.readlines()
f.close()
f = open(final_name, "r")
final = f.readlines()
f.close()
print("Internal coordinate geometry files read")

# extract data from internal coordinate geometries
init_data = []
for line in init:
    init_data.append(float(line))
init_data = np.array(init_data)
final_data = []
for line in final:
    final_data.append(float(line))
final_data = np.array(final_data)
print("Internal coordinate geometry data extracted")

# generate cart2intin
i2ctxt = """ &input
    calctype='int2cart'
 /"""
f = open("./cart2intin", "w")
f.write(i2ctxt)
f.close()
print("cart2intin written")

# generate dummy cartgrd
cartgrdtxt = """    0.739462D-07   0.107719D-01   0.359672D-02
  -0.637601D-07   0.573448D-03   0.113684D-01
  -0.408939D-07  -0.123975D-01  -0.519692D-02
   0.345788D-07  -0.168148D-02  -0.133691D-01
  -0.145659D-07   0.423517D-02   0.559146D-02
   0.106949D-07  -0.150151D-02  -0.199053D-02"""
f = open("./cartgrd", "w")
f.write(cartgrdtxt)
f.close()
print("Dummy cartgrd generated")

# create interpolation vector
interpvec = final_data - init_data
print("Interpolation vector created")

# run this code for each step
def slurmcop(target):
    str_target = str(target)
    print("Starting preparation for " + str_target)
    # generate interpolated geometry as intgeomch
    f = open("./intgeomch", "w")
    g = open("./geoms.txt", "a")
    currgeom = init_data + interpvec*step*target
    g.write(str_target + "\n")
    for coord in currgeom:
        formcoord = format(float(coord), "14.8f") + "\n"
        f.write(formcoord)
        g.write(formcoord)
    f.close()
    g.close()
    # run cart2int to convert to Cartesians
    rv = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./",capture_output=True)
    # read newly-generated Cartesian geometry file
    f = open("./geom.new", "r")
    cart = f.readlines()
    f.close()
    # write to geom.all
    f = open("./geom.all", "a")
    for line in cart:
        f.write(line)
    f.close()
    # write to names.all
    f = open("./names.all", "a")
    f.write(format(target, "5d") + "   " + str_target + "\n")
    f.close()
    # write to energy.all
    f = open("./energy.all", "a")
    f.write("-256.787847331183  -256.787847321778  -256.705819916644  -256.675643170237  -256.667791787388\n")
    f.close()

# run the above function automatically
for i in range(int(1/step) + 21): # +1 was added after
    slurmcop(i) # was i + 1
f = open("./geoms.txt", "a")
f.write("END")
f.close()
print("Wrapped up finishing touch to geoms.txt")

# run dat.x
rv = subprocess.run(["./dat.x"],cwd="./",capture_output=True)
f = open("./dat.log", "w")
f.write(rv.stdout.decode('utf8'))
f.close()
print("All done!")
