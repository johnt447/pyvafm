from vafmbase import Circuit
import math

## Not Gate
# Takes in an Input Signal and if this is greater than 0 it will output a 1.
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in\f$ incoming signal
#
# - Output channels:\n
#   - \f$out = !in\f$

class Not(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):
		
		pass

	def Update (self):
		
		result = 0
		
		if self.I["in"].value > 0:
			result = 1
			
		self.O['out'].value = result
		

## And Gate
# Takes any amount of incoming signals and output 1 if they are all
# strictily positve, 0 otherwise.
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1, in2, ..., inx\f$  incoming signals
#
# - Output channels:\n
#   - \f$out = in_1 \land in_2 \land ... \land in_x \f$


class And(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		# ## Amount of input channels to put in the AND. Default is 2.
		self.factors = 2

		#check if the amount of factors was given	
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		#print '   factors: '+str(self.factors)
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))
		
		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):

		result=1

		for i in self.I.values():
			if i.value < 0:
				result = 0
				break
		
		self.O['out'].value = result

## Or Gate
#Takes in an Input Signal and will output 1 if in1 or in2 are positve numbers
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1 in2\f$
#
# - Output channels:\n
#   - \f$out\f$

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


## XOr Gate
#Takes in an Input Signal and will output 1 if in1 or in2 are positve numbers but will output 0 if both in1 and in2 are positve
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1 in2\f$
#
# - Output channels:\n
#   - \f$out\f$

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

## NOR Gate
#Takes in an Input Signal and will output 1 if in1 and in2 are negative 
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1 in2\f$
#
# - Output channels:\n
#   - \f$out\f$

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
