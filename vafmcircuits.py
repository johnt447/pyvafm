import abc
import itertools
import inspect
import sys
from collections import OrderedDict

#import vafmbase
from vafmbase import Circuit
from vafmbase import ChannelType
from vafmbase import Channel

#import vafmcircuits
#import vafmcircuits_math
#import vafmcircuits_Logic
#import vafmcircuits_signal_processing
#import vafmcircuits_composite


import math
import io


## Virtual Machine class.
#
class Machine(Circuit):
	

	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		## Ordered dictionary of the circuits in the setup.
		self.circuits = OrderedDict()
		
		## Integration timestep
		self.dt = 1.0e-2
		
		## Integer number of update steps so far.
		self._idt = 0;
		
		
		self._MetaI = {}
		
		self._MetaO = {}
		
		self.AddOutput('time')
		
		
		
		self.SetInputs(**keys)
		
		
	
	## Total simulation time.
	@property
	def time(self):
		return self._idt*self.dt
	

	## Create an input channel with the given name.
	# @param name Name of the new input channel.
	def AddInput(self, name):
		
		if name in self.I.keys() or name in self.O.keys():
			raise NameError("A channel named "+name+" already exists in composite circuit "+ str(self))
		
		self.I[name] = Channel(name,self,True)
		self._MetaI[name] = Channel(name,self,False)
	
	## Create an output channel with the given name.
	# @param name Name of the new output channel.
	def AddOutput(self, name):
		
		if name in self.I.keys() or name in self.O.keys():
			raise NameError("A channel named "+name+" already exists in composite circuit "+ str(self))

		self.O[name] = Channel(name,self,False)
		self._MetaO[name] = Channel(name,self,True)

	## Add a circuit of type 'ctype' named 'name' to the setup.
	#
	# This looks into all the loaded modules whose name starts with
	# 'vafmcircuits' and finds the first class named 'ctype'. 
	# It then instantiate the class.
        # - Mandatory arguments:\n
        # 	- type = string: type name of the circuit class\n
        # 	- name = string: name to use for the new instance of the circuit\n
        #
	# @param **argkw Keyworded arguments for circuit initialisation.
	# @return Reference to the created circuit.
	def AddCircuit(self, **argkw):
		
		lst = sys.modules.keys()
		classobj = None

                #check for mandatory arguments, type and name
                if not ("type" in argkw.keys()):
                    raise SyntaxError("The circuit type was not specified.")
                ctype = argkw["type"]
                
                if not ("name" in argkw.keys()):
                    raise SyntaxError("The circuit name was not specified.")
                cname = argkw["name"]

                print "new circuit: " + ctype + "  " + cname
		for i in range(len(lst)): #loop over the modules
			
			if lst[i].startswith('vafmcircuits'): #if the module is a vafmcircuits module
				
				#extract classes from the module, except the abstract one
				c = [s for s in inspect.getmembers(sys.modules[lst[i]], inspect.isclass) if s[0]==ctype]
				
				if len(c)!=0:
					classobj = c[0]
					break
		
		#check if the type was good
		if classobj == None:
			raise NotImplementedError("Circuit "+ctype+" was not implemented or imported!")
		
		#check if the name was good
		if cname in self.circuits.keys():
			raise NameError("A circuit named '"+cname+"' already exists in the setup!")
		
		#instantiate
		instance = classobj[1](machine=self, **argkw)
		self.circuits[cname] = instance
		return instance
	
	## Find the channel with the given tag among the subcircuits.
	# The tag of a channel is a string containing the name of the circuit to which it belongs
	# and the name of the channel separated by a dot.
	# The function raises an error if the circuit does not exist in the dictionary, or if the channel
	# does not exist inside the circuit.
	# The argument chtype is given as enum ChannelType, and if used it will limit the search for the channel
	# only in the input or output channels of the circuit.
	# @param tag Channel tag.
	# @param chtype Type of the channel: ChannelType.Input | ChannelType.Output | ChannelType.Any
	# @return Reference to the channel.
	#
	# \b Example:
	# \code{.py}
	# vafm._GetInternalChannel("oscillator.sin", vafmcore.ChannelType.Output)
	# vafm._GetInternalChannel("integrator.out", vafmcore.ChannelType.Output)
	# vafm._GetInternalChannel("mycircuit.mychannel", vafmcore.ChannelType.Any)
	# \endcode
	def _GetInternalChannel(self, tag, chtype=ChannelType.Any):
		
		ctag = tag.split(".",1)
		if len(ctag) != 2:
			raise SyntaxError ("GetInternalChannel error: channel tag "+tag+ " is invalid.")
		
		cname = ctag[0]
		chname = ctag[1]
		
		allchs = {}
		
		# handle the case where we are looking for a channel of the machine, and not
		# one in a subcircuit.
		if cname == 'global':
			
			raise SyntaxError ("GetInternalChannel error: the VAFM can only perform connections between internal circuits")
		
		#check the name of the circuit
		if not(cname in self.circuits.keys()):
			raise NameError( "GetInternalChannel error: circuit "+cname+" not found." )
		
		#get the circuit
		circ = self.circuits[cname] 
			
		if chtype == ChannelType.Input or chtype == ChannelType.Any:
			allchs.update(circ.I)
		if chtype == ChannelType.Output or chtype == ChannelType.Any:
			allchs.update(circ.O)
		
		return allchs[chname]
		
	
	def _GetMetaChannel(self, tag, chtype=ChannelType.Any):
		
		ctag = tag.split(".",1)
		if len(ctag) != 2:
			raise SyntaxError ("GetMetaChannel error: channel tag "+tag+ " is invalid.")
			
		cname = ctag[0]
		chname = ctag[1]
		
		allchs = {}
		
		# handle the case where we are looking for a channel of the machine, and not
		# one in a subcircuit.
			
		if chtype == ChannelType.Input or chtype == ChannelType.Any:
			allchs.update(self._MetaI)
		if chtype == ChannelType.Output or chtype == ChannelType.Any:
			allchs.update(self._MetaO)
		
		return allchs[chname]
	
	## Find a channel by name.
	# @param chname Name of the channel to find.
	# @return Reference to the channel.
	def GetChannel(self, tag):
		
		#check if the tag has the correct syntax
		chname = tag.split(".",1)
		if len(chname) != 2:
			raise SyntaxError ("Machine.GetChannel error: channel tag "+tag+ " is invalid.")
		cname = chname[0]
		chname = chname[1]
		
		
		if self._IsGlobal(tag):
			circ = self #if the tag is global, the circuit is the machine itself
		else:
			circ = self.circuits
			if not (cname in circ.keys()):
				raise NameError( "Machine.GetChannel error: circuit "+cname+" not found." )
			circ = circ[cname]
		
		#create a global dictionary
		allch = {}
		allch.update(circ.I)
		allch.update(circ.O)
		

		
		if not( chname in allch.keys() ):
			raise NameError( "Machine.GetChannel error: channel "+chname+" not found." )
		
		return allch[chname]
		
	## Checks whether the given channel tag points to a global channel.
	# Global channels are marked as "global.channelname".
	# @param tag String with the channel tag.
	# @return True if the tag points to a global channel, False otherwise.
	def _IsGlobal(self, tag):
		
		ctag = tag.split(".",1)
		if len(ctag) != 2:
			raise SyntaxError ("IsGlobal error: channel tag "+tag+ " is invalid.")
		
		if ctag[0] == 'global':
			return True
		else:
			return False
		
	
	## Connect the output of a circuit to the input of another.
	# The I/O channels to connect are specified with the syntax: "circuit.channel", in the *args arguments
	# array. The first element has to be the output channel to use as source, while all
	# the following elements refer to the destination channels.
	# @param *args Name of the channels to connect: "circuit.channel"
	def Connect(self, *args):
		
		
		#if the output is a global, then it means that we want to connect
		#the global input to input channels in the machine
		
		#find the output channel
		if self._IsGlobal(args[0]):
			outsignal = self._GetMetaChannel(args[0], ChannelType.Input)
		else:
			outsignal = self._GetInternalChannel(args[0], ChannelType.Output)
		
		
		print "connecting " + args[0]
		
		for tag in args[1:]: #for each target input tag
		
			# find the target channel
			if self._IsGlobal(tag):
				target = self._GetMetaChannel(tag, ChannelType.Output)
			else:
				target = self._GetInternalChannel(tag, ChannelType.Input)
			
			print "  -> " + tag
			target.signal = outsignal.signal
	
	
	## Disconnect one or more input channels.
	# This is the same as Disconnect, but it can take multiple "circuit.channel" arguments.
	# @param *args Input channels given as list of strings of format: "circuit.channel"
	def Disconnect(self, *args):

		print "disconnecting: "
		for tag in args:
			
			if self._IsGlobal(tag):
				target = self._GetMetaChannel(tag, ChannelType.Output)
			else:
				target = self._GetInternalChannel(tag, ChannelType.Input)
			print "  - "+ target.name
			target.Disconnect()

	## Initialization.
	#
	# Use this after all circuits and connections are setup.
	# Calls the initialize on each circuit... this is actually useless at the moment!
	def Initialize(self):
		
		for kw in self.circuits.keys():
			self.circuits[kw].Initialize()
	
	## Update cycle.
	#
	# Calls the update routine of each circuit in the setup.
	def Update(self):
		
		#print 'updating machine ' +self.name
		
		for key in self.O.keys(): self.O[key].Push()
		
		# pass the global inputs to metainput
		for key in self.I.keys():
			self._MetaI[key].Set(self.I[key].value)
		#for key in self.I.keys():
		#	self._MetaI[key].Set(self.I[key].value)
		
		for kw in self.circuits.keys():
			
			self.circuits[kw].Update()
			
			if self.circuits[kw].pushed: #push if needed
				self.circuits[kw].Push()
		
		self._idt += 1
		self._MetaO['time'].Set(self.time)
		self.O['time'].Set(self.time)
		#print 'before post' + str(self.O['time'].value)
		
		self.PostUpdate()
	
		#print 'after post' + str(self.O['time'].value)
		
	## Post Update cycle.
	#
	# Called after the Update is finished, to push all buffers.
	def PostUpdate(self):
		
		# pass the metaoutput value to the global output
		for key in self._MetaO.keys():
			self.O[key].value = self._MetaO[key].value
			self._MetaO[key].Push()
		
		#print 'in post 1' + str(self.O['time'].value)
		
		#push the output in the global output if pushed
		if self.pushed:
			for key in self._MetaO.keys(): self.O[key].Push()
		
		#print 'in post 2' + str(self.O['time'].value)
		
		for kw in self.circuits.keys():
			self.circuits[kw].Push()
			
		#print 'in post 3' + str(self.O['time'].value)



## Oscillator circuit.
#
# Creates sine and cosine waves with the specifics given by the inputs.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$amp\f$ amplitude
# 	- \f$freq\f$ frequency
# 	- \f$offset\f$ offset value
#
# - Output channels:
# 	- \f$sin\f$ sine wave \f$ = amp\cdot\sin(2 \pi freq\cdot t) + offset \f$
# 	- \f$cos\f$ cosine wave \f$ = amp\cdot\cos(2 \pi freq\cdot t) + offset \f$
class waver(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		self.AddInput("freq")
		self.AddInput("amp")
		self.AddInput("offset")
		
		self.AddOutput("sin")
		self.AddOutput("cos")

		self.SetInputs(**keys)
		
		
		

	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		
		phase = self.machine.time * self.I["freq"].value
		
		self.O['cos'].value = self.I['amp'].value*math.cos(phase) + self.I['offset'].value
		self.O['sin'].value = self.I['amp'].value*math.sin(phase) + self.I['offset'].value
		
		
		pass

## Output circuit.
#
# Use this to dump the values of channels in a log file.
#
# - Initialisation parameters:\n
# 	- file = name of the log file\n
# 	- dump = #  rate at which data is printed in the file\n
#
# - Input channels:\n
# 	- \f$record\f$  if connected, the output will be printed only when this input is 1\n
#
# - Output channels:\n
# This circuit has no output channel.
class output(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )
		
		if not('file' in keys.keys()):
			raise SyntaxError("Output circuit file not specified!")
		self.filename = keys['file']
		
		if not('dump' in keys.keys()):
			raise SyntaxError("Output circuit dump rate not specified!")
		
		## List of channels to dump in the file.
		self.channels = []
		
		## Dump rate.
		self.dump = keys['dump']
		
		self._file = open(self.filename, 'w')
		
		self._cnt = 0
		
		self.AddInput("record")

		self.SetInputs(**keys)
		
	## Register a channel for output.
	#
	# If the channel is already registered in this output circuit, it won't be registered again.
	def RegisterChannel(self, *args):
		
		#if type(channel) is list:
		#cclist = [j.split(".",1) for j in channel]
		cclist = [self.machine.GetChannel(tag) for tag in args]
		self.channels.extend(cclist)
		#else :
			
		#	if not(channel in self.channels):
		#		self.channels.append(channel)
				


	def Initialize (self):
		
		pass
		
		
		
		
	def Update (self):
		
		self._cnt += 1
		
		if self._cnt == self.dump:
			self._cnt = 0
			#dump the data
			
			for i in self.channels:
				self._file.write(str(i.value)+" ")
			self._file.write('\n')
			
		pass


