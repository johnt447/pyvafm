from vafmbase import Circuit
import math
#import vafmcircuits_Logic
from vafmcircuits import Machine


## \package vafmcircuits_Filters
# This file contains the Filters

## \brief Active Low Pass Filter  circuit.
#
# \image html ActiveLowPass.png "schema"
# Takes a signal in and passes it through a low pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a gain =  Integer:  How much gain the signal will recive 
# 	- \a Q = the Q value of the filter
#	- \a fcut = the frequency cut off for the circuit
# 	- \a pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# 	- signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out = \f$  G \cdot \frac{x(s)}{s^{2} + \frac{ \omega_{c} }{Q} \cdot s + \omega^{2}_{c} } \f$ where \f$ x \f$ is the input signal,  \f$ \omega_{c} = 2 \pi f_c \f$ is the cut off pulse
# 	  \f$ Q \f$  is the quality factor and \f$ G \f$ is the gain.
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='ActiveLowPass', name='ActiveLowFilter', gain = 10, Q= 2, fcutoff= 50, pushed = 'True')
# \endcode
#
class ActiveLowPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
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
		self.x = self.I["signal"].value 

		self.y = self.Gain*self.wc*self.x + (2.0*self.yo-self.yoo) + self.gamma*self.yoo 
		self.y = self.y * self.alpha
		self.O["out"].value=self.y


		self.yoo=self.yo
		self.yo=self.y


## \brief Active High Pass Filter circuit.
#
# \image html ActiveHighPass.png "schema"
# Takes a signal in and passes it through a High pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a Gain =  Integer  How much gain the signal will recive 
# 	- \a pushed = True|False  push the output buffer immediately if True
# 	- \a Q = the Q value of the filter
#	- \a Fcutoff = the frequency cut off for the circuit
#
# \b Input \b channels:
# 	- signal =  incoming signal
#
# \b Output \b channels:
# 	- \a out =\f$ \frac{\omega ^2 _c \cdot x(t) - \frac {y \cdot (t-2dt) - 2 \cdot y \cdot (t-dt)}{dt^2} + \frac{\omega ^2 _c}{2 \cdot Q \cdot dt} y \cdot (t-2dt)  }{ \frac{1}{dt^2} + \frac{\omega ^2 _c}{2 \cdot Q \cdot dt} + \omega ^2 _c  }\f$
#		where \f$ x \f$ is the input signal,  \f$ \omega_{c} = 2 \pi f_c \f$ is the cut off pulse \f$ Q \f$  is the quality factor and \f$ dt \f$ is the timestep.
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='ActiveHighPass', name='ActiveHighFilter', gain = 10, Q= 2, fcutoff= 50, pushed = 'True')
# \endcode
#
class ActiveHighPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
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
		self.x = self.I["signal"].value 
		self.y = (2*self.yo-self.yoo) + self.gamma*self.yoo + self.Gain*(self.xoo-2.0*self.xo+self.x);
		self.y=self.y*self.alpha

		self.O["out"].value=self.y

		self.yoo=self.yo
		self.yo=self.y

		self.xoo=self.xo
		self.xo=self.x


## \brief Active Band Pass Filter  circuit.
#
# \image html ActiveHighPass.png "schema"
# Takes a signal in and passes it through a Band pass filter using the Sallen-Key topology
#
# \b Initialisation \b parameters:
# 	- \a Gain =  Integer  How much gain the signal will recive 
# 	- \a pushed = True|False  push the output buffer immediately if True
# 	- \a Q = the Q value of the filter
#	- \a Fcutoff = the frequency cut off for the circuit
#	- \a Band = The band of frequncies that will be filtered.
#
# \b Input \b channels:
# 	- \a signal = incoming signal
#
# \b Output \b channels:\n
# 	- \a out =\f$ G\frac{Band \cdot dt\cdot(x(t) - x(t-2dt)) + band \cdot dt \cdot (2 \cdot y \cdot (t-dt) - y \cdot (t-2 \cdot dt)) }{ 1 + band \cdot dt + \omega ^2 _c } \f$
#   where \f$ x \f$ is the input signal, \f$ y \f$ is the input signal,  \f$ \omega_{c} = 2 \pi f_c \f$ is the cut off pulse \f$ Q \f$  is the quality factor and \f$ dt \f$ is the timestep.
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='ActiveBandPass', name='ActiveBandFilter', gain = 10, Q= 2, Fcutoff= 50, Band=5 ,pushed = 'True')
# \endcode
#
class ActiveBandPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
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
		self.x = self.I["signal"].value 

		self.y = self.Gain*self.gamma*(self.x-self.xoo) + self.gamma*self.yoo + (2.0*self.yo-self.yoo)

		self.y=self.y*self.alpha

		self.O["out"].value=self.y

		self.yoo=self.yo
		self.yo=self.y

		self.xoo=self.xo
		self.xo=self.x


## \brief Passive Low Pass Filter  circuit.
#
# \image html PassiveLowPass.png "schema"
# Takes a signal in and passes it through a Low pass filter.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
# 	- \a Q = the Q value of the filter
#	- \a Fcutoff = the frequency cut off for the circuit
#	- \a Order = The order of the filter
#
# \b Input \b channels: \n
# 	- \a signal = Incoming signal
#
# \b Output \b channels:\n
# 	- \a out = Filtered signal
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='PassiveLowPass', name='PassiveLowFilter', order = 2, Q= 2, Fcutoff= 50 ,pushed = 'True')
# \endcode
#
class PassiveLowPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
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

		self.filter[0] = self.I["signal"].value 

		for i in range (0, self.Order):
			self.filter[i+1] = self.folds[i] + self.a*(self.filter[i] - self.folds[i]) 

			self.folds[i] = self.filter[i+1]
		self.O["out"].value= self.filter[self.Order]



## \brief Passive High Pass Filter  circuit.
#
#
# \image html PassiveHighPass.png "schema"
# Takes a signal in and passes it through a High pass filter.
#
# \b Initialisation \b parameters:
# 	- \a pushed = True|False  push the output buffer immediately if True
# 	- \a Q = the Q value of the filter
#	- \a Fcutoff = the frequency cut off for the circuit
#	- \a Order = The order of the 
#
# \b Input \b channels:
# 	- \a signal = incoming signal
#
# \b Output \b channels:\n
# 	- \a out = Filtered signal
#
#\b Examples:
# \code{.py}
# machine.AddCircuit(type='PassiveHighPass', name='PassiveHighFilter', order = 2, Q= 2, Fcutoff= 50 ,pushed = 'True')
# \endcode
#
class PassiveHighPass(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		

		self.AddInput("signal")
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

		self.filter[0] = self.I["signal"].value 

		for i in range (1, self.Order+1):
			self.filter[i] = self.a * (self.folds[i] + self.filter[i - 1] - self.folds[i - 1]);

		for i in range (0, self.Order + 1):
			self.folds[i] = self.filter[i]
		self.O["out"].value= self.filter[self.Order -1]
