## Feed object.
# This class contains the numerical value of a channel
# and its buffered value.
class Feed(object):
	
	def __init__(self, ownercircuit):
		
		self.owner = ownercircuit
		
		self._value = 0.0
		self._buff = 0.0
		
	#@property
	def value_get(self):
		return self._value
	
	#@value.setter
	def value_set(self,value):
		self._buff = value
		#print 'buffering value '+str(value)
		
	value = property(value_get, value_set)
	
	def Push(self):
		
		#print 'pushing '+str(self._buff)+' old('+str(self._value)+")"
		self._value = self._buff;
		
	def PushValue(self, value):
		self._value = value
		self._buff = value
	
	

class Channel(object):
	
	def __init__(self, name, owner, isInput):
		
		self.name = name
		self.owner = owner
		self.signal = Feed(owner)
		self.isInput = isInput
	
	#@property
	def value_get(self):
		return self.signal.value
	#@value.setter
	def value_set(self,value):
		self.signal.value = value
		#print 'setting value '+str(value)
		
	value = property(value_get, value_set);
	
	def Push(self):
		self.signal.Push()
	
	def Set(self, value):
		self.signal.PushValue(value)

	## Renew the Feed object so that it is disconnected from everything.
        def Disconnect(self):
            self.signal = Feed(self.owner)

## Abstract circuit class.
#
#
class Circuit(object):

	#__metaclass__ = abc.ABCMeta;
	
	## Common contructor for all circuits.
	#
	# @param machine Reference to the virtual machine.
	# @param name Name of this instance.
	def __init__(self, machine, name):
		
		## Name of the circuit.
		self.name = name
		## Reference to the virtual machine.
		self.machine = machine
		## Push output buffer at the end of Update.
		#
		# If the circuit is pushed, all the output channels will
		# expose the computed value right after the Update routine.
		self.pushed = False
		
		## Dictionary of input channels
		self.I = {}
		## Dictionary of output channels
		self.O = {}
		

	## Default input channels initialisation.
	#
	# Use the keyward arguments **kwargs to set the initial value
	# of input channels. 
	# @param **kwargs Keyworded arguments for circuit initialisation.
	def SetInputs(self, **kwargs):
		
		print 'circuit '+self.name+'('+self.__class__.__name__+') created.'
		
		for key in kwargs.keys():
			
			if key in self.I.keys():
				self.I[key].Set(kwargs[key])
				print '   input '+key+' -> '+str(kwargs[key])
			else:
				print "   " + key + " " + str(kwargs[key])
		
		if 'pushed' in kwargs.keys():
			self.pushed = bool(kwargs['pushed'])
			
		
	## Create an input channel with the given name.
	# @param name Name of the new input channel.
	def AddInput(self, name):
		
		self.I[name] = Channel(name,self,True)
	
	## Create an output channel with the given name.
	# @param name Name of the new output channel.
	def AddOutput(self, name):
		
		self.O[name] = Channel(name,self,False)

	## Find a channel by name.
	# @param chname Name of the channel to find.
	# @return Reference to the channel.
	def GetChannel(self, chname):
		
		isout = chname in self.O.keys()
		isin = chname in self.I.keys()
		
		if not( isout or isin ):
			raise NameError( "Circuit.GetChannel error: channel "+chname+" not found." )
		
		if isout:
			return self.O[chname];
		if isin:
			return self.I[chname];
	

	## Push the buffered value for all output channels.
	def Push(self):
		for kw in self.O.keys():
			self.O[kw].Push()

	
	def __str__( self ):
		return "["+self.__class__.__name__+"]"+self.name

	def Initialize (self):
		raise NotImplementedError( "Should have implemented this" )
		
	def Update (self):
		raise NotImplementedError( "Should have implemented this" )
