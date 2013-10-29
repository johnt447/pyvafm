import numpy 
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine
from scipy.interpolate import LinearNDInterpolator

## \package vafmcircuits_Interpolation
# This file contains the interpolation for the force field.
#


## \brief Interpolation circuit.
#
# This is the circuit that calculates the interpolation of a C-dimensional field in a D-dimensional space.
# The field must be in the following format: 
# <pre> x y z Fx Fy Fz
#         or         
# x y z F
#         or
# x Fx
#         or
# x y Fx Fy </pre>
#
# \b Initialisation \b parameters:
# 	- \a Filename  = Filename of the force field input file.
#	- \a Dimensions = Number of dimensons in the force field.
#	- \a Components	= Number of components of force in the force field.
#
# \b Input \b channels: 
# 	- \a coord : this is the coordiante to calcualte the interpolation.
#
# \b Output \b channels: 
#	- \a Fx: The interpolated forces x component. 
#	- \a Fy: The interpolated forces y component. 
#	- \a Fz: The interpolated forces z component. 
#
# \b Example:
# \code
# field = machine.AddCircuit(type='Interpolate',name='inter', Filename='forces.dat', Dimensons=3, Components=3 , pushed=True)
# \endcode
#
class Interpolate(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		self.AddInput("coord")
		self.AddOutput("Fx")
		self.AddOutput("Fy")
		self.AddOutput("Fz")

		self.minboundarycheck = False
		self.maxboundarycheck = False

		self.Components = 1

		#print self.AddInput("Filename")

		if 'Filename' in keys.keys():
			self.Filename = keys['Filename']
		else:
			raise NameError("Missing Filename input!")

		if 'Dimensions' in keys.keys():
			self.Dimensions = keys['Dimensions']
		else:
			raise NameError("Missing Dimensions input!")

		if 'Components' in keys.keys():
			self.Components = keys['Components']
		else:
			raise NameError("Missing Components input!")


		self.xvalues = []
		self.Fx = []

		self.yvalues = []
		self.Fy = []

		self.zvalues = []
		self.Fz = []


		f= open (self.Filename)

		if self.Dimensions == 1:
			for line in f:
				self.xvalues.append ( line.split()[0] )
				self.Fx.append ( line.split()[self.Dimensions] )
				self.Fy.append ( 0 )
				self.Fz.append ( 0 )




		if self.Dimensions == 2:
			for line in f:
				self.xvalues.append ( line.split()[0] )
				self.Fx.append ( line.split()[self.Dimensions] )

				self.yvalues.append ( line.split()[1] )
				self.Fy.append ( line.split()[self.Dimensions + self.Components - 1] )

				self.Fz.append ( 0 )


		if self.Dimensions == 3 and self.Components == 3:
			for line in f:
				self.xvalues.append ( line.split()[0] )
				self.Fx.append ( line.split()[self.Dimensions ] )

				self.yvalues.append ( line.split()[1] )
  				self.Fy.append ( line.split()[self.Dimensions + self.Components - 2] )

				self.zvalues.append ( line.split()[2] )
				self.Fz.append ( line.split()[self.Dimensions + self.Components - 1] )

		if self.Dimensions == 3 and self.Components == 1:
			for line in f:
				self.xvalues.append ( line.split()[0] )
				self.yvalues.append ( line.split()[1] )
				self.zvalues.append ( line.split()[2] )
				self.Fx.append ( line.split()[self.Dimensions ] )
			self.i = LinearNDInterpolator( (self.xvalues, self.yvalues, self.zvalues ), self.Fx  )

		self.SetInputs(**keys)




		

	def Initialize (self):
		
		pass 
		
	## Setting the maximum x y and z value of the force field
	#
	# @param *args will take in a coordiante  and if the cantilever goes outwith this boundary a warning is printed on screen.
	#
	# \b Example:
	# \code{.py}
	# #For Dimensons = 3
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 3, Components = 3 ,pushed=True)
	# inter.Maxboundary(10,10,10)
	# \endcode
	#		
	# \code{.py}
	# #For Dimensons = 2
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 2, Components = 2 ,pushed=True)
	# inter.Maxboundary(10,10)
	# \endcode
	#
	# \code{.py}
	# #For Dimensons = 1
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 1, Components = 1 ,pushed=True)
	# inter.Maxboundary(10)
	# \endcode

	def Maxboundary(self, *args):
		self.maxx = args[0]

		if len(args) >= 2:
			self.maxy = args[1]
		if len(args) == 3:
			self.maxz = args[2]
		self.maxboundarycheck = True


	## Setting the minimum x y and z value of the force field
	#
	# @param *args will take in a coordiante  and if the cantilever goes outwith this boundary a warning is printed on screen.
	#
	# \b Example:
	# \code{.py}
	# #For Dimensons = 3
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 3, Components = 3 ,pushed=True)
	# inter.Minboundary(0,0,0)
	# \endcode
	#		
	# \code{.py}
	# #For Dimensons = 2
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 2, Components = 2 ,pushed=True)
	# inter.Minboundary(0,0)
	# \endcode
	#
	# \code{.py}
	# #For Dimensons = 1
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 1, Components = 1 ,pushed=True)
	# inter.Minboundary(0)
	# \endcode
	def Minboundary(self, *args):
		self.minx = args[0]
		if len(args) >= 2:
			self.miny = args[1]
		if len(args) == 3:
			self.minz = args[2]

		self.minboundarycheck = True


		
	def Update (self):
		if self.maxboundarycheck == False:
			raise SyntaxError("No max boundarys for the force field added!")

		if self.minboundarycheck == False:
			raise SyntaxError("No min boundarys for the force field added!")
		if self.machine.time > 0:
			if self.I["coord"].value[0] > self.maxx or self.I["coord"].value[0] < self.minx:
				print "Warning tip is outside of the force field (x range) interpolation will output NaN" 
			if self.I["coord"].value[1] > self.maxy or self.I["coord"].value[1] < self.miny:
				print "Warning tip is outside of the force field (y range) interpolation will output NaN"
			if self.I["coord"].value[2] > self.maxz or self.I["coord"].value[2] < self.minz:
				print "Warning tip is outside of the force field (z range) interpolation will output NaN"


		if self.machine.time > 0:
			self.O["Fx"].value =  numpy.interp(self.I["coord"].value[0], self.xvalues,  self.Fx)

		if self.machine.time > 0 and self.Components > 1:
			self.O["Fy"].value =  numpy.interp(self.I["coord"].value[1], self.xvalues,  self.Fy)
		else: 
			self.O["Fy"].value = 0

		if self.machine.time > 0 and self.Components == 3:
			self.O["Fz"].value =  numpy.interp(self.I["coord"].value[2], self.xvalues,  self.Fz)

		if self.machine.time > 0 and self.Components == 1:
			self.O["Fx"].value = self.i.__call__(self.I["coord"].value[0],self.I["coord"].value[1],self.I["coord"].value[2])
			
		else:
			self.O["Fx"].value = 0			
			self.O["Fy"].value = 0
			self.O["Fz"].value = 0
