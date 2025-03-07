# parameters
step = 0.01 # Step size, 0.04 is not bad
init_name = "intc.1MSD" # Path of initial internal coordinate geometry file
final_name = "intc.C2vCI" # Name of final internal coordinate geometry file
refgrab = True # Generate refgrab from geom.all and fit.in
overwrite = False # Overwrite backups

# Before running, make sure you have
#   intg1 and intg2
#   basis.in
#   Hd.CheckPoint
#   dat.x
#   geom.all (if refgrab = True)
#   fit.in   (if refgrab = True)
# This program automatically generates the required files
#   energy.all
#   names.all
#   intcfl
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

mn1 = """ N     7.0    0.00000000   -2.14610702   -1.47203925   14.00307401
 N     7.0    0.00000000    2.14610702   -1.47203925   14.00307401
 N     7.0    0.00000000   -1.40249604   -3.75016651   14.00307401
 N     7.0    0.00000000    1.40249604   -3.75016651   14.00307401
 C     6.0    0.00000000    0.00000000    0.00000000   12.00000000
 H     1.0    0.00000000    0.00000000    2.04557184    1.00782504
"""
c2v = """ N     7.0    0.00000000   -2.01079780   -1.49709856   14.00307400
 N     7.0    0.00000000    2.01079780   -1.49709856   14.00307400
 N     7.0    0.00000000   -1.53986213   -3.73789342   14.00307400
 N     7.0    0.00000000    1.53986213   -3.73789342   14.00307400
 C     6.0    0.00000000    0.00000000    0.01111034   12.00000000
 H     1.0    0.00000000    0.00000000    2.04005294    1.00782504
"""
f = open("./geom", "w")
g = open("./refgeom", "w")
if refgrab:
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
else:
    f.write(c2v)
    g.write(c2v)
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

# generating C2v-symmetrized intcfl
symcoords = """TEXAS                                                                           
K            1.     STRE   1    1.        5.
             1.     STRE        2.        5.
K            1.     STRE   2    3.        1.
             1.     STRE        4.        2.
K                   STRE   3    4.        3.
K                   STRE   4    6.        5.
K          1.0000000BEND   5     2.        1.        5.
          -0.8090170BEND         5.        3.        1.
          -0.8090170BEND         5.        4.        2.
           0.3090170BEND         1.        4.        3.
           0.3090170BEND         2.        3.        4.
K          1.0000000TORS   6     1.        3.        4.        2.
           0.3090170TORS         3.        1.        5.        2.
           0.3090170TORS         4.        2.        5.        1.
          -0.8090170TORS         4.        3.        1.        5.
          -0.8090170TORS         3.        4.        2.        5.
K         -0.5877853TORS   7     3.        4.        2.        5.
           0.5877853TORS         4.        3.        1.        5.
           0.9510565TORS         4.        2.        5.        1.
          -0.9510565TORS         3.        1.        5.        2.
K            1.     OUT    8     6.        2.        1.        5.
K            1.     STRE   9    1.        5.
            -1.     STRE        2.        5.
K            1.     STRE  10    3.        1.
            -1.     STRE        4.        2.
K         -0.5877853BEND  11     5.        3.        1.
           0.5877853BEND         5.        4.        2.
           0.9510565BEND         1.        4.        3.
          -0.9510565BEND         2.        3.        4.
K            1.     BEND  12     1.        6.        5.
            -1.     BEND         2.        6.        5.
  0.50E+01  0.50E+01  0.50E+01  0.62E+01  0.62E+01  0.55E+01  0.15E+01  0.15E+01
  0.33E+00  0.33E+00  0.10E+01  0.10E+01
"""
f = open("./intcfl", "w")
f.write(symcoords)
f.close()
print("intcfl generated")

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
print("Dummy gartgrd generated")

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
