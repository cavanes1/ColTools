# parameter
degencutoff = 350 # cm-1

# import modules
import numpy as np
from os import listdir
from os.path import isfile, join
import os

# read files
# parameters
npoints = 0
enfDiab = 0
eshift = 0
natoms = 0
nstates = 0
h = open("fit.in", "r")
fitin = h.readlines()
h.close()
for param in fitin:
    if "npoints" in param:
        npoints = int(param.split()[-1][:-1])
    elif "enfDiab" in param:
        enfDiab = int(param.split()[-1][:-1])
    elif "eshift" in param:
        eshift = float(param.split()[-1][:-3])
    elif "natoms" in param:
        natoms = int(param.split()[-1])
    elif "nstates" in param:
        nstates = int(param.split()[-1])
print("npoints = " + str(npoints))
print("enfDiab = " + str(enfDiab))
print("eshift  = " + str(eshift))
print("natoms  = " + str(natoms))
print("nstates = " + str(nstates))

# names
f = open("names.all", "r")
namefile = f.readlines()
f.close()
names = []
for line in namefile:
    names.append(line.split()[-1])
print("Finished reading names")

# energies
f = open("energy.all", "r")
abinitenergyfile = f.readlines()
f.close()
f = open("fitener.dat", "r")
surfenergyfile = f.readlines()
f.close()
abinitEs = []
surfEs = []
for state in range(nstates):
    # ab initio energies
    abinitE = []
    for point in range(npoints):
        splitEs = abinitenergyfile[point].split()
        energy = splitEs[state]
        abinitE.append(float(energy))
    abinitEs.append(abinitE)

    # surface energies
    surfE = []
    for point in range(npoints):
        splitEs = surfenergyfile[point].split()
        energy = splitEs[state]
        surfE.append(float(energy))
    surfEs.append(surfE)
abinitEs = (np.array(abinitEs) + eshift)*219474.63067
surfEs = np.array(surfEs)
print("Finished reading energies")

# gradients
abinitG = []
surfG = []
for state in range(1, nstates + 1):
    currAbinitStG = []
    currSurfStG = []
    # ab initio gradients
    f = open("cartgrd.drt1.state" + str(state) + ".all", "r")
    gradfile = f.readlines()
    f.close()
    for point in range(npoints):
        currPtGrad = []
        for atom in range(natoms):
            splitGs = gradfile[natoms*point + atom].split()
            for component in splitGs:
                component = component.replace("D", "E")
                currPtGrad.append(float(component))
        currAbinitStG.append(currPtGrad)
    abinitG.append(currAbinitStG)
    
    # surface gradients
    f = open("cartgrd.drt1.state" + str(state) + ".dat", "r")
    gradfile = f.readlines()
    f.close()
    for point in range(npoints):
        currPtGrad = []
        for atom in range(natoms):
            splitGs = gradfile[natoms*point + atom].split()
            for component in splitGs:
                component = component.replace("D", "E")
                currPtGrad.append(float(component))
        currSurfStG.append(currPtGrad)
    surfG.append(currSurfStG)
abinitG = np.array(abinitG)
surfG = np.array(surfG)
print("Finished reading energy gradients")

# NACs
abinitC = []
surfC = []
for i in range(1, nstates):
    for j in range(i + 1, nstates + 1):
        currAbinitC = []
        currSurfC = []
        # ab initio NACs
        f = open("cartgrd.nad.drt1.state" + str(i) + ".drt1.state" + str(j) + ".all", "r")
        gradfile = f.readlines()
        f.close()
        for point in range(npoints):
            currPtGrad = []
            for atom in range(natoms):
                splitGs = gradfile[natoms*point + atom].split()
                for component in splitGs:
                    component = component.replace("D", "E")
                    currPtGrad.append(float(component))
            currAbinitC.append(currPtGrad)
        abinitC.append(currAbinitC)
        
        # surface NACs
        f = open("cartgrd.nad.drt1.state" + str(i) + ".drt1.state" + str(j) + ".dat", "r")
        gradfile = f.readlines()
        f.close()
        for point in range(npoints):
            currPtGrad = []
            for atom in range(natoms):
                splitGs = gradfile[natoms*point + atom].split()
                for component in splitGs:
                    component = component.replace("D", "E")
                    currPtGrad.append(float(component))
            currSurfC.append(currPtGrad)
        surfC.append(currSurfC)
abinitC = np.array(abinitC)
surfC = np.array(surfC)
print("Finished reading NACs")

# analysis
# energy
nameset = ["C2vCI  ", "1min   ", "2min   ", "SD2-MEX", "1ts    ", "no critical point"]
absEerr = surfEs - abinitEs
for state in range(nstates):
    Eerr = absEerr[state]
    dEsq = np.dot(Eerr, Eerr)/len(Eerr)
    dE = np.sqrt(dEsq)
    print("\nRMS absolute energy error for state " + str(state + 1) + format(dE, "7.1f"))
    ptset = [[], [], [], [], [], []]
    for point in range(npoints):
        if names[point][0] == "C":
            ptset[0].append(Eerr[point])
        elif names[point][0] == "G":
            ptset[1].append(Eerr[point])
        elif names[point][0] == "E":
            ptset[2].append(Eerr[point])
        elif names[point][0] == "S":
            ptset[3].append(Eerr[point])
        elif names[point][0] == "T":
            ptset[4].append(Eerr[point])
        else:
            ptset[5].append(Eerr[point])
    for ptgrp in range(len(nameset)):
        if len(ptset[ptgrp]) > 0:
            dEsq = np.dot(ptset[ptgrp], ptset[ptgrp])/len(ptset[ptgrp])
            dE = np.sqrt(dEsq)
            print("RMS absolute energy error for points near " + nameset[ptgrp] + format(dE, "7.1f"))

# all energies
flatEerr = np.ndarray.flatten(absEerr)
dEsq = np.dot(flatEerr, flatEerr)/(npoints*nstates)
dE = np.sqrt(dEsq)
print("\nRMS absolute energy error (rmsee):")
print("d[E] = " + str(dE))
absabsE = abs(absEerr)
mue = np.sum(absabsE)/(npoints*nstates)
print("Average absolute value of absolute energy error (mue):")
print("<d[E]> = " + str(mue) + "\n")

# energy gradients
nrmgrad = 0
avggrad = 0
inc_grad = 0
for point in range(npoints):
    for state in range(nstates):
        absGerr = abinitG[state][point] - surfG[state][point]
        dgrd = np.dot(absGerr, absGerr)
        gnrm = np.dot(abinitG[state][point], abinitG[state][point])
        dgrd = dgrd/gnrm
        if gnrm > 1e-3:
            nrmgrad += dgrd
            avggrad += np.sqrt(dgrd)
            inc_grad += 1
        else:
            print("Norm of grad = " + str(np.sqrt(gnrm)) + " Norm of error = " + str(np.sqrt(dgrd*gnrm)))
print(str(inc_grad) + " point/states included in gradient RMS analysis\n")

# NACs
nrmcp = 0
inc_cp = 0
for point in range(npoints):
    statepair = -1
    for k in range(nstates-1):
        for l in range(k + 1, nstates):
            statepair += 1
            if (abinitEs[l][point] - abinitEs[k][point]) >= degencutoff:
                inc_cp += 1
                #de1 = max(abs(abinitEs[k][point]-abinitEs[l][point]),1e-5)
                #de2 = max(abs(surfEs[k][point]-surfEs[l][point]),1e-5)
                #dcp = dot_product(dispgeoms(j)%grads(:nvpt,k,l)/de1-fitG(j,:nvpt,k,l)/de2,
                #                  dispgeoms(j)%grads(:nvpt,k,l)/de1-fitG(j,:nvpt,k,l)/de2)
                #ncp = dot_product(dispgeoms(j)%grads(:nvpt,k,l),
                #                  dispgeoms(j)%grads(:nvpt,k,l))/de1**2
                #nrmdcp = nrmdcp + (dcp/ncp)
                
                diff1 = abinitC[statepair][point] + surfC[statepair][point]
                diff2 = abinitC[statepair][point] - surfC[statepair][point]
                #diff = min(abs(diff1), abs(diff2))
                if np.dot(diff1, diff1) < np.dot(diff2, diff2):
                    diff = diff1
                else:
                    diff = diff2
                #dcp = np.dot(abinitC[statepair][point]-surfC[statepair][point], abinitC[statepair][point]-surfC[statepair][point])
                dcp = np.dot(diff, diff)
                ncp = np.dot(abinitC[statepair][point], abinitC[statepair][point])
                nrmcp += (dcp/ncp)
                if dcp > ((4e-2)*ncp):
                    print("Large coupling error at pt" + str(point + 1) + " bkl" + str(k + 1) + str(l + 1) + ": " + str(np.sqrt(dcp/ncp)))
print(str(inc_cp) + " point/states included in coupling RMS analysis")

# final calculations
# gradients
rmseg = np.sqrt(nrmgrad/inc_grad)
mueg = avggrad/inc_grad
print("\nRMS of relative errors of 2-norms of absolute vector difference (rmseg):")
print("d[g] = " + str(rmseg))
print("Average of 2-norms of absolute vector difference errors (mueg):")
print("<d[g]> = " + str(mueg))

# NACs
rmsec=np.sqrt(nrmcp/inc_cp)
print("\nRMS of 2-norms of relative vector difference errors (rmsec):")
print("d[hij] = " + str(rmsec))
