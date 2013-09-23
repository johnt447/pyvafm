from vafmbase import Circuit
import math

## Not Gate
#Takes in an Input Signal and if this signal is greater or equal to 0 it will output a 1.
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in\f$
#
# - Output channels:\n
#   - \f$out\f$

class NotGate(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):
		
		pass

	def Update (self):
		result = 0
		
		if self.I["in"].value >= 0:
			result = 1
			
		self.O['out'].value = result
		

class AndGate(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value >= 0 and self.I["in2"].value >= 0:
			result=1
		self.O['out'].value = result


class OrGate(Circuit):

	def __init__(self, machine, name, **keys):
	
		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")
	
		self.AddOutput("out")

		self.SetInputs(**keys)


	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value >= 0 or self.I["in2"].value >= 0:
			result=1
		self.O['out'].value = result


class XOrGate(Circuit):

	def __init__(self, machine, name, **keys):
	
		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")
	
		self.AddOutput("out")

		self.SetInputs(**keys)


	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value >= 0 or self.I["in2"].value >= 0:
			result=1

		if self.I["in1"].value >= 0 and self.I["in2"].value >= 0:
			result=0

		self.O['out'].value = result


class NORGate(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value <= 0 and self.I["in2"].value <= 0:
			result=1
		self.O['out'].value = result
