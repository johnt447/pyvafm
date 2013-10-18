from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine

## SR Flip Flop circuit.
# This circuit will output 1 if the Signal is high and the reset is low.
# When the reset is high it will output 0.
# 
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	-\f$S\f$ set signal
#	-\f$R\f$ reset signal
#
# - Output channels:\n
#	- \f$Q = \f$ stored bit (0|1)
#	- \f$Qbar = \f$ opposite of the stored bit
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='SRFlipFlop', name='sr')
# \endcode
class SRFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("S")
		self.AddInput("R")

		self.AddOutput("Q")
		self.AddOutput("Qbar")



	def Initialize (self):

		pass




	def Update (self):
	
		if self.I["R"].value > 0:
			self.O["Q"].value = 0
			self.O["Qbar"].value = 1


		if self.I["S"].value > 0 and self.I["R"].value <= 0:
			self.O["Q"].value = 1
			self.O["Qbar"].value = 0



## JK Flip Flop circuit.
# This circuit will output the value of J if J does not eual K, if J and K are 0 then there will be no change, if J is high and K is low then it will output 1 and if both J and K
# are high then it will toggle between Q and Q bar
# 
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	-\f$J\f$
#	-\f$K\f$
#
# - Output channels:\n
# 	- \f$ out = Q \f$
#   - \f$ out = Qbar \f$

class JKFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("J")
		self.AddInput("K")

		self.AddOutput("Q")
		self.AddOutput("Qbar")



	def Initialize (self):

		pass




	def Update (self):		
		if self.I["J"].value > 0 and self.I["K"].value <= 0:
			self.O["Q"].value = 1
			self.O["Qbar"].value = 0

		if self.I["J"].value <= 0 and self.I["K"].value > 0:
			self.O["Q"].value = 0
			self.O["Qbar"].value = 1

		if self.I["J"].value > 0 and self.I["K"].value > 0:
			self.O["Q"].value = self.O["Qbar"].value
			self.O["Qbar"].value = self.O["Q"].value



## D Flip Flop circuit.
#	This circuit is data or delay flip flop. It is dependent on the previous output so will only output high if D is high and previous Q is either low or high. If D is low and
#   the previous Q is high then it will output 0. 
# 
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	-\f$D\f$
#
# - Output channels:\n
# 	- \f$ out = Q \f$
#   - \f$ out = Qbar \f$

class DFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("D")

		self.AddOutput("Q")
		self.AddOutput("Qbar")
		self.Qprevious = 0


	def Initialize (self):

		pass




	def Update (self):		
		if self.I["D"].value <= 0 and self.Qprevious <= 0:
			self.O["Q"].value = 0
			self.O["Qbar"].value = 1

		if self.I["D"].value <= 0 and self.Qprevious > 0:
			self.O["Q"].value = 0
			self.O["Qbar"].value = 1

		if self.I["D"].value > 0 and self.Qprevious <= 0:
			self.O["Q"].value = 1
			self.O["Qbar"].value = 0

		if self.I["D"].value > 0 and self.Qprevious > 0:
			self.O["Q"].value = 1
			self.O["Qbar"].value = 0

			self.Qprevious = self.O["Q"].value



## DR Flip Flop circuit.
#	This circuit is the same as the D flip flop except it includes an reset switch so when R is high the output is 0
# 
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	-\f$D\f$
#	-\f$R\f$
#
# - Output channels:\n
# 	- \f$ Q \f$
#   - \f$ Qbar \f$


class DRFlipFlop(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("D")
		self.AddInput("R")

		self.AddOutput("Q")
		self.AddOutput("Qbar")
		self.Qprevious = 0


	def Initialize (self):

		pass




	def Update (self):		
		if self.I["D"].value <= 0 and self.Qprevious <= 0:
			self.O["Q"].value = 0
			self.O["Qbar"].value = 1

		if self.I["D"].value <= 0 and self.Qprevious > 0:
			self.O["Q"].value = 0
			self.O["Qbar"].value = 1

		if self.I["D"].value > 0 and self.Qprevious <= 0:
			self.O["Q"].value = 1
			self.O["Qbar"].value = 0

		if self.I["D"].value > 0 and self.Qprevious > 0:
			self.O["Q"].value = 1
			self.O["Qbar"].value = 0


		if self.I["R"].value > 0:
			self.O["Q"].value = 0
			self.O["Qbar"].value = 1

		self.Qprevious = self.O["Q"].value
