# -*- coding:utf-8 -*-
## \package vafmcircuits_Interpolation
# This file contains the interpolation for the force field.
# \file vafmcircuits_Interpolation.py
# This file contains the interpolation for the force field.

import numpy
import math
from vafmbase import Circuit
from scipy.interpolate import LinearNDInterpolator
import ctypes

## \brief Tri-linear interpolation circuit.
#
# This is the circuit that calculates the interpolation of the provided force field. 
# The force field must be in the following format, but plese note that the interpolation 
# circuit is capable of taking any number of dimensions and components in, 
# but for a case where there is an unequal amount of dimensions and components the 
# unused components column must be filled with zeros. 
# Except in the case of 3 dimensions and 1 component, this can be left as it is. 
# Examples of how the force fields must be formated is shown below.: \n
# <pre> x y z Fx Fy Fz or x y z F or x y z Fx 0 0 or x y Fx 0 <pre>
#
# - \b Initialisation \b parameters:
#         - \a Filename = Filename of the force field input file.
#         - \a Dimensions = Number of dimensons in the force field.
#         - \a Components = Number of components of force in the force field.
#
# - \b Input \b channels:
# - \a coord : this is the coordiante to calcualte the interpolation.
#
# - \b Output \b channels:
# - \a Fx: The interpolated forces where x is the component for example F1 would be first first component.
#
# \b Example:
# \code
# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensions = 3, Components = 3 ,pushed=True)
# \endcode
#

class i3Dlin(Circuit):
    
    
	def __init__(self, machine, name, **keys):        
			
		super(self.__class__, self).__init__( machine, name )

		#filename = "forces.dat"
		#components = 3
		#dim = 3

		if 'filename' in keys.keys():
			filename = keys['filename']
			print "filename = " +str(filename)
		else:
			raise NameError("No filename entered ")

		if 'comp' in keys.keys():
			components = keys['comp']
			print "components = " +str(components)
		else:
			raise NameError("No components entered ")

		if 'dim' in keys.keys():
			dim = keys['dim']
			print "dim = " +str(dim)
		else:
			raise NameError("No dim entered ")


		if 'xstep' in keys.keys():
			xstep = keys['xstep']
			print "xstep = " +str(xstep)
		else:
			raise NameError("No xstep entered ")

		if 'ystep' in keys.keys():
			ystep = keys['ystep']
			print "ystep = " +str(ystep)
		else:
			raise NameError("No ystep entered ")
		
		if 'zstep' in keys.keys():
			zstep = keys['zstep']
			print "zstep = " +str(zstep)
		else:
			raise NameError("No zstep entered ")


		self.AddInput("x")
		self.AddInput("y")
		self.AddInput("z")
		
		for i in range(0,components):
			self.AddOutput("F"+str(i+1))
		

		comp = [ [] for _ in range( components ) ]
		pos = [ [] for _ in range( dim ) ]

		f = open(filename, "r")
		for line in f:
			for i in range(0,components):
				comp[i].append( float(line.split()[i + dim]) )

			for i in range(0,dim):
				pos[i].append( float(line.split()[i]) )



		Circuit.cCore.Add_i3Dlin.argtypes = [ctypes.c_int #Core Id
			,ctypes.POINTER(ctypes.c_double) #testarr
			,ctypes.c_int #size
			,ctypes.c_int #components

			,ctypes.c_double #zstep
			,ctypes.c_double #ystep
			,ctypes.c_double #zstep

			,ctypes.c_double #xmin
			,ctypes.c_double #ymin
			,ctypes.c_double #zmin

			,ctypes.c_int #sizex
			,ctypes.c_int #sizey
			,ctypes.c_int #sizez

			,ctypes.c_double #xmax
			,ctypes.c_double #ymax
			,ctypes.c_double] #zmax 

		size = len(comp[0])
		coord=[]
		for i in range(0,components):
			for j in range(0,size):
					coord.append(comp[i][j])

		xmin = pos[0][0]
		ymin = pos[1][0]
		zmin = pos[2][0]


		xmax = pos[0][-1]
		ymax = pos[1][-1]
		zmax = pos[2][-1]


		sizey = int(pos[2][-1]/zstep - pos[2][0]/zstep +1 )*components
		sizex = int( (pos[1][-1]/ystep - pos[1][0]/ystep+1) * sizey +1 )

		sizez = int(len(pos[2]))



		test_arr = (ctypes.c_double * len(coord))(*coord)
		self.cCoreID = Circuit.cCore.Add_i3Dlin(machine.cCoreID
			 , test_arr
			 , size
			 , components
			 , ctypes.c_double (xstep)
			 , ctypes.c_double(ystep)
			 , ctypes.c_double(zstep)
			 , ctypes.c_double (xmin)
			 , ctypes.c_double(ymin)
			 , ctypes.c_double(zmin)
			 , sizex
			 , sizey
			 , sizez
			 , ctypes.c_double (xmax)
			 , ctypes.c_double(ymax)
			 , ctypes.c_double(zmax))

		self.SetInputs(**keys)

