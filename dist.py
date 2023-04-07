# parameters
init_cart_name = input("Name (or path) of initial Cartesian geometry file: ")
final_cart_name = input("Name (or path) of final Cartesian geometry file: ")

# module import
import numpy as np
import os
import subprocess
print("Modules imported")

# read given Cartesian geometry files
f = open(init_cart_name, "r")
init_cart = f.readlines()
f.close()
f = open(final_cart_name, "r")
final_cart = f.readlines()
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
g1cart = np.array(g1cart)
final_cart_data = []
for line in final_cart:
    final_cart_data.append(line.split())
g2cart = []
for atom in final_cart_data:
    g2cart.append(float(atom[2])) # x coordinate
    g2cart.append(float(atom[3])) # y coordinate
    g2cart.append(float(atom[4])) # z coordinate
g2cart = np.array(g2cart)
print("Cartesian geometry data extracted")

# create directories
allitems = os.listdir(".")
if "G1" not in allitems:
    os.system("mkdir G1")
os.system("cp " + init_cart_name + " G1/geom")
if "G2" not in allitems:
    os.system("mkdir G2")
os.system("cp " + final_cart_name + " G2/geom")

# generate intcin
conv = 0.529177211 # Angstroms per Bohr radii
# initial geometry
f = open("G1/intcin", "w")
f.write("TEXAS\n")
for atom in init_cart_data:
    f.write("  " + atom[0]
            + format(float(atom[1]), "17.5f")
            + format(float(atom[2])*conv, "10.5f")
            + format(float(atom[3])*conv, "10.5f")
            + format(float(atom[4])*conv, "10.5f") + "\n")
f.close()
# final geometry
f = open("G2/intcin", "w")
f.write("TEXAS\n")
for atom in final_cart_data:
    f.write("  " + atom[0]
            + format(float(atom[1]), "17.5f")
            + format(float(atom[2])*conv, "10.5f")
            + format(float(atom[3])*conv, "10.5f")
            + format(float(atom[4])*conv, "10.5f") + "\n")
f.close()
print("intcin generated")

# run intc to generate intcfl
# initial geometry
rv = subprocess.run(["/home/cavanes1/col/Columbus/intc.x"],cwd="./G1",capture_output=True)
print("G1 intc output:")
print(rv.stdout.decode('utf8'))
# final geometry
rv = subprocess.run(["/home/cavanes1/col/Columbus/intc.x"],cwd="./G2",capture_output=True)
print("G2 intc output:")
print(rv.stdout.decode('utf8'))
# ensure both directories have the same intcfl file for consistency
os.system("mv G2/intcfl G2/intcflg2")
os.system("cp G1/intcfl G2")

# generate internal coordinates from Cartesian coordinates
# generate cart2intin
c2itxt = """ &input
    calctype='cart2int'
 /"""
f = open("G1/cart2intin", "w")
f.write(c2itxt)
f.close()
f = open("G2/cart2intin", "w")
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
f = open("G2/cartgrd", "w")
f.write(cartgrdtxt)
f.close()
# run cart2int
rv = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./G1",capture_output=True)
rv2 = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./G2",capture_output=True)
print("Initial cart2int output:")
print(rv.stdout.decode('utf8'))
print("Final cart2int output:")
print(rv2.stdout.decode('utf8'))

# read internal coordinate files
f = open("G1/intgeom", "r")
init_int = f.readlines()
f.close()
init_int_data = []
for line in init_int:
    init_int_data.append(float(line))
init_int_data = np.array(init_int_data)
f = open("G2/intgeom", "r")
final_int = f.readlines()
f.close()
final_int_data = []
for line in final_int:
    final_int_data.append(float(line))
final_int_data = np.array(final_int_data)
print("Internal geometry files read")

# reverse cart2intin direction in 0
i2ctxt = """ &input
    calctype='int2cart'
 /"""
f = open("G1/cart2intin", "w")
f.write(i2ctxt)
f.close()
f = open("G2/cart2intin", "w")
f.write(i2ctxt)
f.close()
print("cart2intin direction reversed in directories")

# ensure G2 is oriented at same location as G1
os.system("cp G1/geom G1/geom.old")
os.system("mv G2/geom G2/geom.old")
os.system("cp G1/geom G2")
os.system("cp G1/intgeom G1/intgeomch")
os.system("cp G2/intgeom G2/intgeomch")

# run cart2int to convert to Cartesians
rv = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./G1",capture_output=True)
rv2 = subprocess.run(["/home/cavanes1/col/Columbus/cart2int.x"],cwd="./G2",capture_output=True)
print("cart2int output for first geometry:")
print(rv.stdout.decode('utf8'))
print("cart2int output for second geometry:")
print(rv2.stdout.decode('utf8'))

# extract data from newly generated Cartesian geometries
f = open("G1/geom.new", "r")
new1 = f.readlines()
f.close()
f = open("G2/geom.new", "r")
new2 = f.readlines()
f.close()
print("Cartesian geometry files read")
g1data = []
for line in new1:
    g1data.append(line.split())
g1data = np.array(init_cart_data)
g1ncart = []
for atom in g1data:
    g1ncart.append(float(atom[2])) # x coordinate
    g1ncart.append(float(atom[3])) # y coordinate
    g1ncart.append(float(atom[4])) # z coordinate
g1ncart = np.array(g1ncart)
g2data = []
for line in new2:
    g2data.append(line.split())
g2data = np.array(final_cart_data)
g2ncart = []
for atom in g2data:
    g2ncart.append(float(atom[2])) # x coordinate
    g2ncart.append(float(atom[3])) # y coordinate
    g2ncart.append(float(atom[4])) # z coordinate
g2ncart = np.array(g2ncart)
print("Cartesian geometry data extracted")

# calculate initial Cartesian difference (geom)
cartidiff = g2cart - g1cart
print("\nGeometry difference vector for input Cartesian geometries:")
print(cartidiff)
cartidist = np.linalg.norm(cartidiff)
print("Distance = " + str(cartidist) + " Bohr radii")

# calculate new Cartesian difference (geom.new)
cartndiff = g2ncart - g1ncart
print("\nGeometry difference vector for generated Cartesian geometries:")
print(cartndiff)
cartndist = np.linalg.norm(cartndiff)
print("Distance = " + str(cartndist) + " Bohr radii")

# calculate internal coordinate difference
intdiff = final_int_data - init_int_data
print("\nGeometry difference vector for internal coordinates:")
print(intdiff)
for coordinate in range(len(intdiff)):
    print("Coordinate " + str(coordinate + 1) + ": " + str(intdiff[coordinate]))
intdist = np.linalg.norm(intdiff)
print("Distance = " + str(intdist) + " (unknown units)")
