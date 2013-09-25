from vafmbase import Circuit
import math
import vafmcore

## Min/Max value circuit.
#
# Takes in an input and a CheckTime value then it will output the max and min value over that given time period and repeat until the total program time has elapsed
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#	- CheckTime = This is the peroid which the circuit will check for max and min values, for example if a checktime of 
#     0.5 is chosen and the total program time is 2 then the circuit will output 4 values of min and max
#
# - Input channels:\n
# 	- \f$inf$
#	-\f$CheckTime = integer$
#
# - Output channels:\n
# 	- \f$max = maximum value over the given peroid $
#	- \f$max = minimum value over the given peroid $
#	- \f$amp = \frac{max-min}{2} $
#	- \f$amp = \frac{max-min}{2} $


class minmax(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		#check if checktime is used in the input file
		if 'CheckTime' in keys.keys():
			self.checktime = keys['CheckTime']
		else:
			raise NameError("Missing CheckTime input!")
		#calculate how many steps are needed for the given timestep
		self.timesteps= self.checktime/self.machine.dt

		self.counter=0

		self.AddInput("in")
		
		#create output channels
		self.AddOutput("max")
		self.AddOutput("min")
		self.AddOutput("amp")
		self.AddOutput("offset")

		self.SetInputs(**keys)
		#setting min and max to the first value in the input file
		self.min=self.I["in"].value
		self.max=self.I["in"].value


	def Initialize (self):
		
		pass
		

		
		
	def Update (self):
		#if the value is greater or less than min or max then reassign the max and min values
		if self.I["in"].value > self.max:
			self.max=self.I["in"].value
		if self.I["in"].value < self.min:
			self.min=self.I["in"].value
		#add one to the counter
		self.counter=self.counter + 1
		#only print out values that are not 0 when the counter is = to timesteps
		self.O['max'].value = 0
		self.O['min'].value = 0
		
		#if the counter is equal to the amount of time steps then then output the values
		if self.timesteps == self.counter:

			self.O['max'].value = self.max
			self.O['min'].value=self.min

			self.O['amp'].value = (self.max - self.min)/2
			self.O['offset'].value = (self.max + self.min)/2

			#reset min and max for the next calculation
			self.min=self.I["in"].value
			self.max=self.I["in"].value


			self.counter=0

## Differentation circuit.
#
# Takes in a input and returns the derivative
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#	
#
# - Input channels:\n
# 	- \f$inf$
#
# - Output channels:\n
# 	- \f$out = /frac{din}{dt}$

class derivative(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		self.AddInput("in")
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)

		
		
		self.y=self.I["in"].value

	def Initialize (self):
		
		pass
	
		
		
	
	def Update (self):


		
		self.yo=self.y
		self.y = self.I["in"].value

		result=(self.y-self.yo)/(self.machine.dt)

		self.O['out'].value = result

## Integration circuit.
#
# Takes in a input and returns the integral
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#	
#
# - Input channels:\n
# 	- \f$inf$
#
# - Output channels:\n
# 	- \f$out = \int_a^\b \mathrm{in}\,\mathrm{d}t$


class integral(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		self.AddInput("in")
		
		#create output channels
		self.AddOutput("out")
		
		self.SetInputs(**keys)

		
		
		self.yo=0
		self.result = 0

	def Initialize (self):
		
		pass
	
		
		
	
	def Update (self):

	 		self.result +=  ( (self.yo + self.I["in"].value)*(self.machine.dt)*0.5 )

			self.O['out'].value = self.result
			self.yo = self.I["in"].value


class Delay(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		self.AddInput("in")

	def Initialize (self):
		
		pass
	
		
		
	
	def Update (self):



