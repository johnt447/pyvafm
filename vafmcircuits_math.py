## \file vafmcircuits_math.py
# This file contains the basic arithmetic operator circuits.
#
#

from vafmbase import Circuit
import math


## Arithmetic sum circuit.
#
# Sums up the input signals 'in#' and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
# - Initialisation parameters:
# 	- factors = # number of input channels
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1, in2, ..., inx\f$  incoming signals
#
# - Output channels:\n
# 	- \f$out = \sum_i^{factors} in_i \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opAdd', name='adder')
# machine.AddCircuit(type='opAdd', name='summer', factors=4)
# machine.AddCircuit(type='opAdd', name='summer', in2=3.5)
# \endcode
class opAdd(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		## Amount of input channels to sum. Default is 2.
		self.factors = 2
		
		#check if the amount of factors was given	
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		#print '   factors: '+str(self.factors)
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		
		result = 0
		
		for i in self.I.values():
			result += i.value
			
		self.O['out'].value = result

## Arithmetic subtraction circuit.
#
# Outputs the difference between two input signals 'in#' in the output 'out'.
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1, in2\f$  input signals
#
# - Output channels:\n
# 	- \f$out = in_1 - in_2 \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opSub', name='minus')
# machine.AddCircuit(type='opSub', name='minus', in2=3.5)
# \endcode
#
class opSub(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#create input channels
		self.AddInput("in1")
                self.AddInput("in2")
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
        
	def Update (self):
		
		result = self.I["in1"].value - self.I["in2"].value
		self.O['out'].value = result


## Arithmetic multiplier circuit.
#
# Multiplies the input signals 'in#' and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
# - Initialisation parameters:
# 	- factors = # number of input channels
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1, in2, ..., inx\f$  incoming signals
#
# - Output channels:
# 	- \f$out = \prod_i^{factors} in_i \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opMul', name='mul')
# machine.AddCircuit(type='opMul', name='mul', factors=4)
# machine.AddCircuit(type='opMul', name='mul', in2=0.4)
# \endcode
#
class opMul(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#check if the amount of factors was given	
		self.factors = 2
		if 'factors' in keys.keys():
			self.factors = int(keys['factors'])
		#print '   factors: '+str(self.factors)
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("in"+str(i+1))
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)
		

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		
		result = 1

		for i in self.I.values():
			result *= i.value
		
		self.O['out'].value = result


## Arithmetic division circuit.
#
# Outputs the ratio between two input signals 'in#' in the output 'out'.
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in1, in2\f$  input signals
#
# - Output channels:\n
# 	- \f$out = in_1 / in_2 \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opDiv', name='div')
# machine.AddCircuit(type='opDiv', name='div', in2=0.5)
# \endcode
#
class opDiv(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#create input channels
		self.AddInput("in1")
		self.AddInput("in2")
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
        
	def Update (self):
		
		result = self.I["in1"].value / self.I["in2"].value
		self.O['out'].value = result


## Arithmetic linear-combo circuit.
#
# Computes the linear combination of the input signals 'ina#' and 'inb#',
# and outputs the result in 'out'.
# The amount of input signals is set with the 'factors=#' argument when
# the circuit is created.
#
# - Initialisation parameters:\n
# 	- factors = # number of factors\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	- \f$ina1, ina2, ..., inax\f$  incoming signals\n
# 	- \f$inb1, inb2, ..., inbx\f$  incoming signals\n
#
# - Output channels:\n
# 	- \f$out = \sum_i^{factors} ina_i\times inb_i \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opLinC', name='combo')
# machine.AddCircuit(type='opLinC', name='combo', factors=4)
# machine.AddCircuit(type='opLinC', name='combo', inb1=5.2)
# \endcode
#
class opLinC(Circuit):

	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		#check if the amount of factors was given	
		self.factors = 2
		if 'factors' in keys.keys():
			self.factors = keys['factors']
		#print '   factors: '+str(self.factors)
		
		#create input channels
		for i in range(self.factors):
			self.AddInput("ina"+str(i+1))
			self.AddInput("inb"+str(i+1))
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)
		

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		
		result = 0
		
		for i in range(self.factors):
			result += self.I["ina"+str(i+1)].value * self.I["inb"+str(i+1)].value
			
		self.O['out'].value = result


## Absolute value circuit.
#
# Takes in an inpute and returns the Absolute vcalue of it
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	- \f$in\f$ incoming signal
#
# - Output channels:\n
# 	- \f$out = |in|\f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opAbs', name='abs')
# \endcode
#
class opAbs(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )


		self.AddInput("in")
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
		
		
	def Update (self):
		
		result = self.I["in"].value
		
		if self.I["in"].value < 0:
			result = self.I["in"].value * -1
		
		self.O["out"].value = result



## Power value circuit.
#
# Takes in an inpute and returns the result raised to a given power
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#	- power = integer The value the function result will be raised by
#
# - Input channels:\n
# 	- \f$in\f$ incoming signal
#
# - Output channels:\n
# 	- \f$out = in^{power}\f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='opPow', name='pow', power=3.45)
# \endcode
#
class opPow(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		if 'power' in keys.keys():
			self.power = keys['power']
		else:
			raise SyntaxError("ERROR! power not specified.")

		self.AddInput("in")
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)

	def Initialize (self):
		
		pass
		
		
		
	def Update (self):
		
		result = math.pow(self.I["in"].value,  self.power)
		
		self.O["out"].value = result
