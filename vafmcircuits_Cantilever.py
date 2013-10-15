import numpy 
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine

class Cantilever(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		if 'ForceField' in keys.keys():
			self.ForceField = keys['ForceField']
		else :
			raise NameError("Missing ForceField input! (the ForceField input is the object which is assigned to the interpolate circuit, see examples")


	def Initialize (self):
		
		pass 

	def Update (self):
		
		pass


