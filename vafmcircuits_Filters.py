from vafmbase import Circuit
import math
#import vafmcircuits_Logic
from vafmcircuits import Machine

## Active Low Pass Filter  circuit.
#
# Takes a signal in and passes it through a low pass filter using the Sallen-Key topology
#
# - Initialisation parameters:
# 	- gain =  Integer  How much gain the signal will recive 
# 	- Q = the Q value of the filter
#	- fcut = the frequency cut off for the circuit
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$in\f$  incoming signal
#
# - Output channels:\n
# 	- \f$out =\f$ Put Equation here
#

class ActiveLowPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("in")
		self.AddOutput("out")


		self.Gain=math.pi*0.5
		if 'gain' in keys.keys():
			self.Gain = keys['gain']
		else:
			print "WARNING! No gain give, using default gain = "+str(self.Gain)
			#raise NameError("Missing gain!")


		self.Q=math.sqrt(2.0)*0.5
		if 'Q' in keys.keys():
			self.Q = keys['Q']
		else:
			print "WARNING! No Q give, using default Q = "+str(self.Q)
			#raise NameError("Missing Q!")


		self.Fcutoff=0
		if 'fcut' in keys.keys():
			self.fc = keys['fcut']
		else:
			raise NameError("Missing fcut!")



		self.wc = 2* math.pi * self.fc * machine.dt
		self.gamma = self.wc/(2*self.Q)

		self.wc=self.wc*self.wc
		self.alpha=1/(1 + self.gamma + self.wc)

		self.y=0
		self.yo=0
		self.yoo=0
		self.x = 0
		self.y = 0

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		self.x = self.I["in"].value 

		self.y = self.Gain*self.wc*self.x + (2.0*self.yo-self.yoo) + self.gamma*self.yoo 
		self.y = self.y * self.alpha
		self.O["out"].value=self.y


		self.yoo=self.yo
		self.yo=self.y


## Active High Pass Filter  circuit.
#
# Takes a signal in and passes it through a High pass filter using the Sallen-Key topology
#
# - Initialisation parameters:
# 	- Gain =  Integer  How much gain the signal will recive 
# 	- pushed = True|False  push the output buffer immediately if True
# 	- Q = the Q value of the filter
#	- Fcutoff = the frequency cut off for the circuit
#
# - Input channels:
# 	- \f$in\f$  incoming signal
#
# - Output channels:\n
# 	- \f$out =\f$ Put Equation here
class ActiveHighPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("in")
		self.AddInput("Gain")
		self.AddInput("Q")
		self.AddInput("Fcutoff")

		self.AddOutput("out")


		self.Gain=0
		if 'Gain' in keys.keys():
			self.Gain = keys['Gain']
		else:
			raise NameError("Missing Gain!")


		self.Q=0
		if 'Q' in keys.keys():
			self.Q = keys['Q']
		else:
			raise NameError("Missing Q!")


		self.Fcutoff=0
		if 'Fcutoff' in keys.keys():
			self.fc = keys['Fcutoff']
		else:
			raise NameError("Missing Fcutoff!")



		self.wc = 2* math.pi * self.fc * machine.dt
		self.gamma = self.wc/(2*self.Q)

		self.alpha=1/(1 + self.gamma + self.wc*self.wc)

		self.y=0
		self.yo=0
		self.yoo=0
		self.x = 0
		self.xo=0
		self.xoo=0

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		self.x = self.I["in"].value 
		self.y = (2*self.yo-self.yoo) + self.gamma*self.yoo + self.Gain*(self.xoo-2.0*self.xo+self.x);
		self.y=self.y*self.alpha

		self.O["out"].value=self.y

		self.yoo=self.yo
		self.yo=self.y

		self.xoo=self.xo
		self.xo=self.x


## Active Band Pass Filter  circuit.
#
# Takes a signal in and passes it through a Band pass filter using the Sallen-Key topology
#
# - Initialisation parameters:
# 	- Gain =  Integer  How much gain the signal will recive 
# 	- pushed = True|False  push the output buffer immediately if True
# 	- Q = the Q value of the filter
#	- Fcutoff = the frequency cut off for the circuit
#	- Band = The band of frequncies that will be filtered.
#
# - Input channels:
# 	- \f$in\f$  incoming signal
#
# - Output channels:\n
# 	- \f$out =\f$ Put Equation here


class ActiveBandPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("in")
		self.AddInput("Gain")
		self.AddInput("Q")
		self.AddInput("Fcutoff")

		self.AddOutput("out")


		self.Gain=0
		if 'Gain' in keys.keys():
			self.Gain = keys['Gain']
		else:
			raise NameError("Missing Gain!")


		self.Q=0
		if 'Q' in keys.keys():
			self.Q = keys['Q']
		else:
			raise NameError("Missing Q!")


		self.Fcutoff=0
		if 'Fcutoff' in keys.keys():
			self.fc = keys['Fcutoff']
		else:
			raise NameError("Missing Fcutoff!")

		self.band=0
		if 'Fcutoff' in keys.keys():
			self.band = keys['Band']
		else:
			raise NameError("Missing Band!")

		self.gamma = self.band
		self.wc = self.fc
		self.gamma = self.wc/self.gamma

		self.wc = 2 * math.pi * self.wc * machine.dt
		self.gamma = self.wc /(2*self.gamma)

		self.alpha = 1/(1 + self.gamma + self.wc*self.wc)

		self.y=0
		self.yo=0
		self.yoo=0
		self.x = 0
		self.xo=0
		self.xoo=0

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		self.x = self.I["in"].value 

		self.y = self.Gain*self.gamma*(self.x-self.xoo) + self.gamma*self.yoo + (2.0*self.yo-self.yoo)

		self.y=self.y*self.alpha

		self.O["out"].value=self.y

		self.yoo=self.yo
		self.yo=self.y

		self.xoo=self.xo
		self.xo=self.x


## Passive Low Pass Filter  circuit.
#
# Takes a signal in and passes it through a Low pass filter.
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
# 	- Q = the Q value of the filter
#	- Fcutoff = the frequency cut off for the circuit
#	- Order = The order of the 
#
# - Input channels:
# 	- \f$in\f$  incoming signal
#
# - Output channels:\n
# 	- \f$out =\f$ Put Equation here


class PassiveLowPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("in")
		self.AddInput("Fcutoff")
		self.AddInput("Order")
		self.AddOutput("out")


		self.Fcutoff=0
		if 'Fcutoff' in keys.keys():
			self.fc = keys['Fcutoff']
		else:
			raise NameError("Missing Fcutoff!")


		self.Order=0
		if 'Order' in keys.keys():
			self.Order = keys['Order']
		else:
			raise NameError("Missing Order!")

		self.fc = 1/(2*math.pi * self.fc)
		self.a = machine.dt/(self.fc +self.fc)


		self.x = 0

		self.folds = [0]* (self.Order + 1)
		self.filter = [0] * (self.Order +1)
		print self.folds
	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):

		self.filter[0] = self.I["in"].value 

		for i in range (0, self.Order):
			self.filter[i+1] = self.folds[i] + self.a*(self.filter[i] - self.folds[i]) 

			self.folds[i] = self.filter[i+1]
		self.O["out"].value= self.filter[self.Order]



## Passive High Pass Filter  circuit.
#
# Takes a signal in and passes it through a High pass filter.
#
# - Initialisation parameters:
# 	- pushed = True|False  push the output buffer immediately if True
# 	- Q = the Q value of the filter
#	- Fcutoff = the frequency cut off for the circuit
#	- Order = The order of the 
#
# - Input channels:
# 	- \f$in\f$  incoming signal
#
# - Output channels:\n
# 	- \f$out =\f$ Put Equation here


class PassiveHighPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("in")
		self.AddInput("Fcutoff")
		self.AddInput("Order")
		self.AddOutput("out")


		self.Fcutoff=0
		if 'Fcutoff' in keys.keys():
			self.fc = keys['Fcutoff']
		else:
			raise NameError("Missing Fcutoff!")


		self.Order=0
		if 'Order' in keys.keys():
			self.Order = keys['Order']
		else:
			raise NameError("Missing Order!")

		self.fc = 1/(2*math.pi * self.fc)
		self.a = self.fc/(machine.dt +self.fc)


		self.x = 0

		self.folds = [0]* (self.Order + 1)
		self.filter = [0] * (self.Order +1)
		print self.folds
	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):

		self.filter[0] = self.I["in"].value 

		for i in range (1, self.Order+1):
			self.filter[i] = self.a * (self.folds[i] + self.filter[i - 1] - self.folds[i - 1]);

		for i in range (0, self.Order + 1):
			self.folds[i] = self.filter[i]
		self.O["out"].value= self.filter[self.Order -1]
