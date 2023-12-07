# required files
#   The geometry to be analyzed, in COLUMBUS Cartesian format
#   If provided = True, intcfl in the directory this program is being run from

# parameters
provided = False
init_cart_name = input("Name (or path) of Cartesian geometry file: ")

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# read given Cartesian geometry files
f = open(init_cart_name, "r")
init_cart = f.readlines()
f.close()
print("Cartesian geometry files read")

# extract data from Cartesian geometries
init_cart_data = []
for line in init_cart:
    init_cart_data.append(line.split())
g1cart = []
for atom in init_cart_data:
    g1cart.append(float(atom[2])) # x coordinate
    g1cart.append(float(atom[3])) # y coordinate
    g1cart.append(float(atom[4])) # z coordinate
print("\ng1cart:\n")
print(g1cart)
g1cart = np.array(g1cart)
print("\nCartesian geometry data extracted")

# create directories
allitems = os.listdir(".")
if "G1" not in allitems:
    os.system("mkdir G1")
os.system("cp " + init_cart_name + " G1/geom")

if provided:
    os.system("cp intcfl G1")
else:
    # generate intcin
    conv = 0.529177211 # Angstroms per Bohr radii
    f = open("G1/intcin", "w")
    f.write("TEXAS\n")
    for atom in init_cart_data:
        f.write("  " + atom[0]
                + format(float(atom[1]), "17.5f")
                + format(float(atom[2])*conv, "10.5f")
                + format(float(atom[3])*conv, "10.5f")
                + format(float(atom[4])*conv, "10.5f") + "\n")
    f.close()

    # run intc to generate intcfl
    rv = subprocess.run(["/home/cavanes1/col/Columbus/intc.x"],cwd="./G1",capture_output=True)
    print("G1 intc output:")
    print(rv.stdout.decode('utf8'))

# generate internal coordinates from Cartesian coordinates
# generate cart2intin
c2itxt = """ &input
    calctype='cart2int'
 /"""
f = open("G1/cart2intin", "w")
f.write(c2itxt)
f.close()
# generate dummy cartgrd
cartgrdtxt = """    0.739462D-07   0.107719D-01   0.359672D-02
  -0.637601D-07   0.573448D-03   0.113684D-01
  -0.408939D-07  -0.123975D-01  -0.519692D-02
   0.345788D-07  -0.168148D-02  -0.133691D-01
  -0.145659D-07   0.423517D-02   0.559146D-02
   0.106949D-07  -0.150151D-02  -0.199053D-02"""
f = open("G1/cartgrd", "w")
f.write(cartgrdtxt)
f.close()
# run cart2int
rv = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./G1",capture_output=True)
print("cart2int output:")
print(rv.stdout.decode('utf8'))

# read internal coordinate files
f = open("G1/intgeom", "r")
init_int = f.readlines()
f.close()
init_int_data = []
for line in init_int:
    init_int_data.append(float(line))
print("init_int_data:\n")
print(init_int_data)
init_int_data = np.array(init_int_data)
print("\nInternal geometry files read")
