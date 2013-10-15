import numpy 
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine

class Interpolate(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		self.AddInput("Filename")
		self.AddInput("Dimensions")
		#print self.AddInput("Filename")

		if 'Filename' in keys.keys():
			self.Filename = keys['Filename']
		else:
			raise NameError("Missing Filename input!")

		if 'Dimensions' in keys.keys():
			self.Dimensions = keys['Dimensions']
		else:
			raise NameError("Missing Dimensions input!")


		self.xvalues = []
		self.Fx = []

		self.yvalues = []
		self.Fy = []

		self.zvalues = []
		self.Fz = []


		f= open ("data.txt")

		if self.Dimensions == 1:
			for line in f:
				self.xvalues.append ( line.split()[0] )
				self.Fx.append ( line.split()[1] )


		if self.I["Dimensions"].value == 2:
			for line in f:
				self.xvalues.append ( line.split()[0] )
				self.Fx.append ( line.split()[2] )

				self.yvalues.append ( line.split()[1] )
				self.Fy.append ( line.split()[3] )


		if self.I["Dimensions"].value == 3:
			for line in f:
				self.xvalues.append ( line.split()[0] )
				self.Fx.append ( line.split()[3] )

				self.yvalues.append ( line.split()[1] )
  				self.Fy.append ( line.split()[4] )

				self.zvalues.append ( line.split()[2] )
				self.Fz.append ( line.split()[5] )

		self.SetInputs(**keys)

	def Initialize (self):
		
		print 
		
	def Outputx(self, *args):
		point = args[0]

		return numpy.interp(point, self.xvalues, self.Fx )
		

	def Outputy(self, *args):
		point = args[0]

		return numpy.interp(point, self.yvalues, self.Fy )

	def Outputz(self, *args):
		point = args[0]

		return numpy.interp(point, self.zvalues, self.Fz )
		
	def Update (self):
		
		pass

