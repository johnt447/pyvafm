from vafmbase import Circuit
import math


## Template composite circuit
#
# Sums up the input signals 'in#' and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
class composite(Circuit):
	
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		## Name of the composite template.
		self.typename = "template"
		
		#self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		
		pass

	def __str__( self ):
		return "[composite:"+self.typename+"]"+self.name
		
