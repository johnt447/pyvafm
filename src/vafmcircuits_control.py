## \file vafmcircuits_control.py
# This file contains the controller circuits.

from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel

import math


## PI circuit.
#
# This circuit will compare the input signal with a reference signal and 
# regulate the output in order to minimise the difference using a PI controller.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	- \f$signal\f$ incoming signal
# 	- \f$set\f$ reference signal
# 	- \f$Kp\f$ proportional constant
# 	- \f$Ki\f$ integral constant
#
# - Output channels:\n
# 	- \f$out = K_p (set-signal) + K_i \int (set-signal) dt \f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='PI', name='pi')
# machine.AddCircuit(type='PI', name='pi', Kp=0.1)
# machine.AddCircuit(type='PI', name='pi', Kp=0.2, Ki=0.01)
# \endcode
class PI(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddInput("Kp")
		self.AddInput("Ki")
		self.AddInput("set")
		
		self.AddOutput("out")

		self.delta = 0
		self.integral=0
		self.oldInt=0
		
		self.SetInputs(**keys)

	def Initialize (self):

		pass



	def Update (self):

		self.delta =  self.I["set"].value - self.I["signal"].value
		self.integral = self.integral + ( 0.5*(self.oldInt + self.I["Ki"].value*self.delta)*self.machine.dt  )
		self.O["out"].value = self.delta * self.I["Kp"].value + self.integral
		self.oldInt = self.I["Ki"].value * self.delta


## PID circuit.
#
# This circuit will compare the input signal with a reference signal and 
# regulate the output in order to minimise the difference using a PID controller.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
# 	- Kp = Proportionality tuning constant
#	- Ki = Integral tuning constant
#	- Kd = Derivative tuning constant
# - Input channels:\n
# 	- \f$signal\f$ incoming signal
# 	- \f$set\f$ reference signal
# 	- \f$Kp\f$ proportional constant
# 	- \f$Ki\f$ integral constant
# 	- \f$Kd\f$ derivative constant
#
# - Output channels:\n
# 	- \f$out = K_p (set-signal) + K_i \int (set-signal) dt +K_d\frac{d(set-signal)}{dt}\f$
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='PID', name='pid')
# machine.AddCircuit(type='PID', name='pid', Kp=0.1)
# machine.AddCircuit(type='PID', name='pid', Kp=0.2, Ki=0.01, Kd=0.1)
# \endcode
class PID(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddInput("Kp")
		self.AddInput("Ki")
		self.AddInput("Kd")
		self.AddInput("set")
		self.AddOutput("out")

		self.delta = 0
		self.integral=0
		self.oldInt=0
		self.olddelta = 0
		#self.counter = 0 # I didnt see why this was here?

		self.SetInputs(**keys)

	def Initialize (self):

		pass




	def Update (self):
	
		self.delta =  self.I["set"].value - self.I["signal"].value
		self.integral = self.integral + ( 0.5*(self.oldInt + self.I["Ki"].value*self.delta)*self.machine.dt  )
		
		#if self.counter > 0: #i removed this if...
		self.O["out"].value = self.delta * self.I["Kp"].value + self.integral + self.I["Kd"].value *(self.delta-self.olddelta)/self.machine.dt
		
		self.oldInt = self.I["Ki"].value * self.delta
		self.olddelta = self.delta
		#self.counter = self.counter + 1


## Limiter circuit.
#
# This circuit will limit a signal from going above the max and below the min values.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	- \f$signal\f$ incoming signal
# 	- \f$min\f$ minimum value
# 	- \f$max\f$ maximum value
#
# - Output channels:\n
# 	- \f$out = Max(Min(in, max), min)\f$
#
# \b Example:
# \code{.py}
# machine.AddCircuit(type='limiter', name='lim')
# machine.AddCircuit(type='limiter', name='lim', min=-10.0)
# machine.AddCircuit(type='limiter', name='lim', min=0.0, max=99999)
# \endcode
#
class limiter(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddInput("min")
		self.AddInput("max")
		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):

		pass


	def Update (self):
	
		self.O["out"].value =  max(min(self.I["signal"].value, self.I["max"].value), 
			self.I["min"].value)


