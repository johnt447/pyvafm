from vafmbase import Circuit
import vafmcore
import math


## Template composite circuit
#
# Sums up the input signals 'in#' and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
# \code{.py}
# asd
# asd lol
# \endcode
#
class composite(Circuit):
	
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		
		## Virtual machine containing the subcircuits.
		self._machine = vafmcore.VAFM()
		
		#check if the amount of factors was given	
		if not ('assembly' in keys.keys()):
			raise SyntaxError("The assembly function for the composite circuit was not specified.")
		
		self._Assemble = keys["assembly"]
		
		print "*** Assembling ... ***"
		self._Assemble(self)
		print "*** Assembly Done! ***"
		
		self.SetInputs(**keys)

	## Assemble the composite.
	# This function is deliberately not implemented and the user \b must define it
	# and replace the original one.
	#
	def _Assemble (self):
		raise NotImplementedError( "This function has to be reassigned from the main script." )

	## Add a circuit of type 'ctype' named 'name' inside the composite circuit.
	#
	# This looks into all the loaded modules whose name starts with
	# 'vafmcircuits' and finds the first class named 'ctype'. 
	# It then instantiate the class.
        # - Mandatory arguments:\n
        # 	- type = string: type name of the circuit class\n
        # 	- name = string: name to use for the new instance of the circuit\n
        #
	# @param **argkw Keyworded arguments for circuit initialisation.
	# @return Reference to the created circuit.
	def AddCircuit(self, **argkw):
		
		self._machine.AddCircuit(**argkw)

	## Connect the output of a circuit to the input of another.
	# The I/O channels to connect are specified with the syntax: "circuit.channel", in the *args arguments
	# array. The first element has to be the output channel to use as source, while all
	# the following elements refer to the destination channels.
	# @param *args Name of the channels to connect: "circuit.channel"
	def Connect(self, *args):
		
		self._machine.Connects(*args)


	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		
		pass

	def __str__( self ):
		return "[composite:"+self.typename+"]"+self.name
		
