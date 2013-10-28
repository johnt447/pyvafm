from vafmbase import Circuit
import math
import vafmcircuits

## \package vafmcircuits_signal_processing
# This file contains the signal processing circuits for example min/max and delay.
#


## \brief Gain circuit.
#
# \image html gain.png "schema"
# Takes in an input signal and multiplies it by a given gain
# 
#
# \b Initialisation \b parameters:
# - pushed = True|False  push the output buffer immediately if True
# - gain = integer 
#
# \b Input \b channels:
# - \a signal 
#
# \b Output \b channels:
# - \a out =  signal \f$ \cdot \f$ gain 
#
# 
# \b Example:
# \code{.py}
# machine.AddCircuit(type='gain', name='Gain' , gain = 10)
# \endcode
#
class gain(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in")
		self.AddOutput("out")

		if 'gain' in keys.keys():
			self.gain = keys['gain']
		else:
			raise NameError("Missing gain parameter!")


	def Initialize (self):

		pass


	def Update (self):		
		self.O['out'].value  = self.I['in'].value*self.gain



## Min/Max value circuit.
#
# Takes in an input and a CheckTime value then it will output the max and min
# value over that given time period and repeat until the total program
# time has elapsed.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#	- CheckTime = This is the peroid which the circuit will check for max and min values, for example if a checktime of 
#     0.5 is chosen and the total program time is 2 then the circuit will output 4 values of min and max
#
# - Input channels:\n
# 	- \f$inf\f$
#	- \f$CheckTime = integer\f$
#
# - Output channels:\n
# 	- \f$max = maximum value over the given peroid \f$
#	- \f$max = minimum value over the given peroid \f$
#	- \f$amp = \frac{max-min}{2} \f$
#	- \f$amp = \frac{max-min}{2} \f$


class minmax(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		#check if checktime is used in the input file
		if 'CheckTime' in keys.keys():
			self.checktime = keys['CheckTime']
		else:
			raise NameError("Missing CheckTime input!")
		#calculate how many steps are needed for the given timestep
		self.timesteps = int(self.checktime/self.machine.dt)

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
# 	- \f$in\f$
#
# - Output channels:\n
# 	- \f$out =  \frac{din}{dt} \f$
#
class derivative(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in")

		#create output channels
		self.AddOutput("out")

		self.SetInputs(**keys)


		#@todo i dont understand this it should always be 0 anyway!
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
# 	- \f$in\f$
#
# - Output channels:\n
# 	- \f$out = \int_0^t in dt \f$
#
#
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

## Delay circuit.
#
# Takes in a input and delays the start of the circuit by a fixed amount of inputted time
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#	- DelayTime = Integer
#
# - Input channels:\n
# 	- \f$in\f$
#	- \f$DelayTime\f$
#
# - Output channels:\n
# 	- \f$out = In_{t-DelayTime}\f$

class Delay(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in")
		self.AddOutput("out")

		if 'DelayTime' in keys.keys():
			self.delaytime = keys['DelayTime']
		else:
			raise NameError("Missing DelayTime input!")

		self.steps = self.delaytime/self.machine.dt
		self.counter = 0
		self.counteroutput = 0

		self.bufferinput = []




	def Initialize (self):

		pass




	def Update (self):
	
		if self.counter * self.machine.dt <= self.delaytime:
			self.O["out"].value = 0

		self.bufferinput.append(self.I["in"].value)
		self.counter = self.counter + 1

		if self.counter * self.machine.dt  > self.delaytime: 
			self.O["out"].value = self.bufferinput[self.counteroutput]

			self.counteroutput = self.counteroutput+1



## Peak Detector circuit.
#
# Takes in an input and outputs when it finds a peak, where the peak is and how long since the last peak
# - Upper Peak found if $f(t-2) < f(t-1) and f(t-1) > f(t) $ is true
# - Lower Peak found if $f(t-2) > f(t-1) and f(t-1) < f(t) $ is true
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#	- up = 1|0 1 means find peaks in the positve y axis and 0 means find peaks in the negative 
#
# - Input channels:\n
# 	- \f$in\f$
#	-\f$up = 1|0 \f$
#
# - Output channels:\n
# 	- \f$ tick = \f$ 1 if a peak and 0 if no peak 
# 	- \f$ peak = \f$ location of the peak
# 	- \f$ delay = \f$ time elapsed since last peak was found
#
#
class PeakDetector(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		if 'up' in keys.keys():
			self.up = keys['up']
			if self.up == 1:
				self.upordown=True
			if self.up == 0:
				self.upordown = False

		else:
			raise NameError("Missing up or down selection!")
		
		self.AddInput("in")
		self.AddOutput("tick")
		self.AddOutput("peak")
		self.AddOutput("delay")


		self.counter=0
		self.yoo=0
		self.yo=0
		self.y=0

		self.peak = 0
		self.tick = 0
		self.delay = 0
		self.startcounter = False


	def Initialize (self):
		
		pass


	def Update (self):
		self.yoo= self.yo
		self.yo = self.y
		self.y= self.I["in"].value
		self.tick=0

		if self.yoo < self.yo and self.yo > self.y and self.upordown == True:
			self.tick = 1 
			self.peak = self.yo
			self.delay = self.counter * self.machine.dt
			self.counter=0

		if self.yoo > self.yo and self.yo < self.y and self.upordown == False:
			self.tick = 1  
			self.peak= self.yo
			self.delay = self.counter * self.machine.dt
			self.counter = 0

		self.counter=self.counter + 1

		self.O["peak"].value = self.peak
		self.O["tick"].value = self.tick
		self.O["delay"].value = self.delay


## Phasor circuit.
#
# Takes in two inputs and will measure the legnth of time between the first
# input becoming postive and the second also becoming positive.
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	- \f$in1\f$
#	- \f$in2\f$
#
# - Output channels:\n
# 	- \f$ tick =\f$ 1 when input 2 becomes positve assuming input 1 has alreayd become postive before it
# 	- \f$ delay =\f$ time difference between input 1 and input 2 becoming positve 

class Phasor(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		self.AddInput("in1")
		self.AddInput("in2")
		self.AddOutput("tick")
		self.AddOutput("delay")

		self.counter= 0
		self.check = False



	def Initialize (self):

		pass




	def Update (self):
		
		if	self.I["in1"].value > 0 and self.I["in2"].value < 0:
			self.counter = self.counter +1
			self.check= True

		#@todo are you sure these 2 lines should not be indented under the if?
		self.O["tick"].value = 0
		self.O["delay"].value = 0

		if self.I["in2"].value > 0 and self.check == True:
			self.O["tick"].value = 1
			self.O["delay"].value = self.counter * self.machine.dt
			self.counter = 0
			self.check = False


## Flip circuit.
#
# Takes in and input and will output a tick everytime the signal changes 
# from negative to positive.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	-\f$inf\f$
#
# - Output channels:\n
# 	- \f$ out = 1 when f(t-1) <= 0 and f(t) >0 \f$
#

class Flip(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		self.AddInput("in")
		self.AddOutput("out")
		self.yo= 0

	def Initialize (self):

		pass
	
		
		
	
	def Update (self):
		
		self.O["out"].value = 0
		
		if	self.I["in"].value > 0 and self.yo < 0:
			self.O["out"].value = 1
		
		self.yo=self.I["in"].value



