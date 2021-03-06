#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pylab import *
from optparse import OptionParser

def buck_pot(a, rho, c, cut):
	# Buckingham potential
	array_size = int(cut/0.01)
	buck = np.zeros(shape = (array_size, 2))
	for x in range (1, array_size):
		buck[x, 0] = x*0.01
		buck[x, 1] = a*np.exp(-buck[x, 0]/rho) - c**6/buck[x, 0]**6
	return buck

def coulomb_pot(q1, q2, cut):
	# Coulombic interaction
	array_size = int(cut/0.01)
	coul = np.zeros(shape = (array_size, 2))
	for x in range (1, array_size):
		coul[x, 0] = x*0.01
		#covert Hartree to eV and Amstrom to Bohr
		coul[x, 1] = 27.211396132*(q1*q2)/(x*0.01*1.889725989)
	return coul

def lennard_pot(A, B, cut):
	# Lennard potential
	array_size = int(cut/0.01)
	lenn = np.zeros(shape = (array_size, 2))
	for x in range (1, array_size):
		lenn[x, 0] = x*0.01
		lenn[x, 1] = A/((x*0.01)**12) - B/((x*0.01)**6)
	return lenn

# specify input file
parser = OptionParser()
parser.add_option("-f", "--file",
                  action = "store", type = "string", dest = "file", default = "GULP.gin",
                  help = "Path to input file [default: ./geometry.in]")
(options, args) = parser.parse_args()
file = options.file
		
# Open the file and split into Lines
f = open(file,"r")
lines = f.readlines()
f.close()

A = 0
B = 0
buckinghams = []
coulomb = []
lennard = []
# Start reading lines
for line in lines:
	 inp = line.split()
	 if inp == []:
	  continue
	 if len(inp) == 12:
		buckinghams.append(inp)
	 elif len(inp) == 3 and inp[1] == "core":
		coulomb.append(inp)
	 elif len(inp) == 3 and inp[1] == "shel":
		coulomb.append(inp)
	 elif len(inp) == 10:
		lennard.append(inp)

for i in buckinghams:
	buck = buck_pot(float(i[4]), float(i[5]), float(i[6]), float(i[8])) 
	for j in coulomb:
		if j[0] == i[0] and j[1] == i[1]:
			q1 = j[2]
		if j[0] == i[2] and j[1] == i[3]:
			q2 = j[2]
	coul = coulomb_pot(float(q1), float(q2), float(i[8]))
	for k in lennard:
		if k[0] == i[0] and k[2] == i[2]:
			A = k[4]
                        B = k[5]
		# in case element order is reversed in input file
		elif k[2] == i[0] and k[0] == i[2]:
			A = k[4]
			B = k[5]
        lenn_j = lennard_pot(float(A), float(B), float(i[8]))
        #total_pot = np.add(buck,coul,lenn_j)
	total_pot = buck+coul+lenn_j
	
	plt.plot(buck[1:, 0],buck[1:, 1], label = 'Buckingham potential')
	plt.plot(coul[1:, 0], coul [1:, 1], label = 'Coulombic interaction')
	plt.plot(lenn_j[1:, 0], lenn_j[1:, 1], label = 'Lennard potential')
	plt.plot(buck[1:, 0], total_pot[1:, 1], label = 'Total potential')
	plt.legend(('Buckingham potential', 'Coulombic interaction', 'Lennard potential', 'Total potential'))
	plt.axis([0.00, 5.00, -100, 100])
	plt.xlabel('Interatomic distance, r', fontsize = 16)
	plt.ylabel('Potential Energy, eV', fontsize = 16)
	plt.title("%s" % (str(i[0] + " (" + i[1] + ")" + " - " + i[2] + " (" + i[1] + ")")), fontsize = 18)
	xticklines = getp(gca(), 'xticklines')
	yticklines = getp(gca(), 'yticklines')
	xgridlines = getp(gca(), 'xgridlines')
	ygridlines = getp(gca(), 'ygridlines')
	xticklabels = getp(gca(), 'xticklabels')
	ygridlines = getp(gca(), 'ygridlines')
	xticklabels = getp(gca(), 'xticklabels')
	yticklabels = getp(gca(), 'yticklabels')

	setp(xticklines, 'linewidth', 3)
	setp(yticklines, 'linewidth', 3)
	#setp(xgridlines, 'linestyle', '-')
	#setp(ygridlines, 'linestyle', '-')
	setp(yticklabels, 'color', 'Black', fontsize='medium')
	setp(xticklabels, 'color', 'Black', fontsize='medium')
	plt.grid(True)
	plt.savefig('%s.eps' % (str(i[0] + i[2])))
	plt.show()
