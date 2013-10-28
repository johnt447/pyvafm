## \file vafmcircuits_avg.py
# This file contains the averager circuit classes.

from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel

import math
import numpy

## Averager circuit.
#
# This circuit will return the average of an input signal, over a certain amount of time.
# If the
# The output is updated only when the buffer
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
# 	- time = sampling time (in real time units)
#	- moving = True|False  compute average at each step (True) or only when the buffer is full (False, default)
#
# - Input channels:\n
# 	- \f$in\f$ signal to average
#
# - Output channels:\n
# 	- \f$out\f$ averaged signal
#
class avg(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddOutput("out")

		self._time = 0.01
		self._steps = 10
		self._cnt = 0
		self._moving = False
		
		if 'time' in keys.keys():
			self._time = float(keys['time'])
		else:
			raise NameError("Missing time parameter!")
		
		self._steps = math.floor(self._time/self.machine.dt)
		self._buffer = numpy.zeros(self._steps)
		
		if 'moving' in keys.keys():
			self._moving = bool(keys['moving'])

		self.SetInputs(**keys)

		self.tot = 0

	def Initialize (self):

		pass
	

	def Update (self):
		
		#record the value
		self.tot -= self._buffer[self._cnt] #remove the value to overwrite from total
		self._buffer[self._cnt] = self.I['signal'].value #record
		
		#add it to the total
		self.tot += self.I['signal'].value
		
		#increment the counter and refit it...
		self._cnt = (self._cnt+1) % self._steps
		
		if self._moving: #if computing moving avg...
			#output average
			self.O['out'].value = self.tot/self._steps
		else:
			if self._cnt == 0:
				self.O['out'].value = self.tot/self._steps
				
		
		
