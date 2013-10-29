from vafmbase import Circuit
import math

## \package vafmcircuits_Logic
# This file contains the basic logic operator circuits.

## \brief Not Gate
# \image html Not.png "schema"
#
# Truth Table for a Not Gate
#
# Input 		|Output
# ------------- | ------------- 
# 1 			| 0             
# 0			    | 1				
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a signal = incoming signal
#
# \b Output \b channels:
#   - \a out = \! signal
#
# \b Example:
# \code
# machine.AddCircuit(type='Not',name='scann'pushed=True)
# \endcode
#
class Not(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):
		
		pass

	def Update (self):
		
		result = 0
		
		if self.I["signal"].value > 0:
			result = 1
			
		self.O['out'].value = result
		

## And Gate
# \image html And.png "schema"
#
# Truth table for an And Gate
# Input A		|Input B		|Output
# ------------- | ------------- | ------------- 
# 0 			| 0             | 0             
# 0			    | 1				| 0           
# 1			    | 0				| 0           
# 1			    | 1				| 1           
#
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a in1, \a in2, ..., \a inx =  incoming signals
#
# \b Output \b channels:\n
#   - \a out = \f$ in_1  \land in_2  \land ...  \land in_x \f$
#
# \b Example:
# \code
# machine.AddCircuit(type='And',name='And'pushed=True)
# \endcode
#
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
# \image html OrGate.png "schema"
#
# Truth table for a Or Gate
# Input A		|Input B		|Output
# ------------- | ------------- | ------------- 
# 0 			| 0             | 0             
# 0			    | 1				| 1           
# 1			    | 0				| 1           
# 1			    | 1				| 1    
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a in1, \a in2 = incoming signal 
#
# \b Output \b channels:\n
#   - \a out = if in1 or in2 >0 output 1 otherwise output 0
#
# \b Example:
# \code
# machine.AddCircuit(type='OrGate',name='OrGate'pushed=True)
# \endcode
#
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
# \image html XOrGate.png "schema"
#
# Truth table for a XOr Gate
# Input A		|Input B		|Output
# ------------- | ------------- | ------------- 
# 0 			| 0             | 0             
# 0			    | 1				| 1           
# 1			    | 0				| 1           
# 1			    | 1				| 0    
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	-  \a in1, \a in2 = incoming signal
#
# \b Output \b channels:\n
#   - \a out = if in1 or in2 >0 output 1 but if both in1 and in2 > 0 then output 0, otherwise output 0
#
# \b Example:
# \code
# machine.AddCircuit(type='XOrGate',name='XorGate'pushed=True)
# \endcode
#
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
# \image html NOrGate.png "schema"
#
# Truth table for a NOr Gate
# Input A		|Input B		|Output
# ------------- | ------------- | ------------- 
# 0 			| 0             | 1             
# 0			    | 1				| 0           
# 1			    | 0				| 0           
# 1			    | 1				| 0    
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- \a in1, \a in2 = incoming signal
#
# \b Output \b channels:
#   - \a out = will output 1 if in1 and in2 are < 1 otherwise will output 0
#
# \b Example:
# \code
# machine.AddCircuit(type='NORGate',name='NORGate'pushed=True)
# \endcode
#
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
