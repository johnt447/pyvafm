## \example example_composite.py

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


## Virtual Machine main class.
#
# The vitual machine is effectively a Circuit, with input/output channels,
# but it also contains an internal assembly of circuits that run during the Update
# cycle. Every machine always has the output channel 'time' created during initialisation.
#
#
class Machine(Circuit):


	def __init__(self, machine=None, name="machine", **keys):
		
		super(self.__class__, self).__init__( machine, name )

		## Ordered dictionary of the circuits in the setup.
		self.circuits = OrderedDict()

		## Integration timestep
		self.dt = 0.0
		if not ('dt' in keys.keys()):
			print 'WARNING! No timestep dt was given in the initialisation parameters.'
		else:
			self.dt = keys['dt']
		
		## Integer number of update steps so far.
		self._idt = 0;

		
		self._MetaI = {}

		self._MetaO = {}

		self.AddOutput('time')

		if 'assembly' in keys.keys():
			self.Assemble = keys['assembly']
			self.Assemble(self)

		self.SetInputs(**keys)


	## Fabricator function.
	# 
	# This function is called when the machine is instantiated, only if
	# the "assembly" parameter was given among initialisation arguments.
	# The function is originally left unimplemented, so the user can build
	# the setup after the machine is instantiated.
	#
	# \b Example:
	# \code{.py}
	# ...
	# # assembly function definition
	# def MyAssembly(compo):
	# 
	#   # add global channels
  	#   compo.AddInput("signal1")
  	#   ...
  	#   # add internal circuits
  	#   compo.AddCircuit(type='opAdd',name='adder',factors=2, pushed=True)
  	#   ...
  	#   # connect internal circuits to global input and outputs
  	#   compo.Connect("global.signal1","adder.in1")
  	#   compo.Connect("adder.out","global.out")
	#   ...
	# 
	# # main script
	# def main():
	#  
	#   main = Machine(name='machine', dt=0.01, pushed=True);
	#   
	#   # add a Machine circuit to main, and set it up with the MyAssembly function
  	#   main.AddCircuit(type='Machine', name='compo1', assembly=MyAssembly, pushed=True)
  	#   ...
	#  
	# if __name__ == '__main__':
	#   main()
	# \endcode
	def Assemble(self):
		pass

	## Total simulation time.
	@property
	def time(self):
		return self._idt*self.dt


	## Create an input channel with the given name.
	#
	# Add a global input channel to the machine. This is done when the
	# machine is intended to be used as a composite circuit inside another machine,
	# and thus it needs to communicate with other circuits.
	#
	# @param name Name of the new input channel.
	#
	# \b Example:
	# \code{.py}
	# machine = Machine(name='machine', dt=0.01);
	# machine.AddInput('signal')
	# \endcode
	#
	def AddInput(self, name):

		if name in self.I.keys() or name in self.O.keys():
			raise NameError("A channel named "+name+" already exists in composite circuit "+ str(self))

		self.I[name] = Channel(name,self,True)
		self._MetaI[name] = Channel(name,self,False)

	## Create an output channel with the given name.
	#
	# Add a global output channel to the machine. This is done when the
	# machine is intended to be used as a composite circuit inside another machine,
	# and thus it needs to communicate with other circuits.
	#
	# @param name Name of the new output channel.
	#
	# \b Example:
	# \code{.py}
	# machine = Machine(name='machine', dt=0.01);
	# machine.AddOutput('outsignal')
	# \endcode
	#
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
    #	- others: specific arguments depending on the particular circuit to add.
    #
	# - Optional arguments:\n
    # 	- pushed = bool: defined the output behaviour model.\n
    #	- others: specific arguments depending on the particular circuit to add.
    #
    # 
    # @param **argkw Keyworded arguments for circuit initialisation.
    #
	# @return Reference to the created circuit.
	#
    # \b Example:
	# \code{.py}
	# machine = Machine(name='machine', dt=0.01);
	#
	# machine.AddCircuit(type='opAdd',name='adder',factors=2, pushed=True)
	# machine.AddCircuit(type='output',name='log',file='log.log', dump=1)
	# \endcode
	#
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


	## Find a channel by tag.
	#
	# The tag is given in the string format: "circuitname.channelname".
	# Global circuits of the machine are named "global.channelname".
	#
	# @param tag Channel tag
	#
	# @return Reference to the channel.
	#
	# \b Example:
	# \code{.py}
	# sinwave = machine.GetChannel('waver.sin')
	# time = machine.GetChannel('global.time')
	# \endcode
	#
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
	#
	# The I/O channels to connect are specified with the syntax: "circuit.channel", in the *args arguments
	# array. The first element has to be the output channel to use as source, while all
	# the following elements refer to the destination channels.
	#
	# @param *args Name of the channels to connect: "circuit.channel"
	#
	# \b Example:
	# \code{.py}
  	# main = Machine(name='machine', dt=0.01, pushed=True);
  	# 
  	# main.AddCircuit(type='waver', name='osc', amp=1, freq=1)
  	# main.AddCircuit(type='opAdd', name='adder', factors=2)
  	#
  	# main.Connect("osc.sin", "adder.in1")
  	# main.Connect("osc.cos", "adder.in2")
  	#
	# \endcode
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
	#
	# This is the same as Disconnect, but it can take multiple "circuit.channel" arguments.
	#
	# @param *args Input channels given as list of strings of format: "circuit.channel"
	#
	# \b Example:
	# \code{.py}
	# machine.Disconnect('waver.amp')
	# machine.Disconnect('adder.in1', 'adder.in2')
	# \endcode
	#
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
	# 
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

		self._PostUpdate()

		#print 'after post' + str(self.O['time'].value)

	## Post Update cycle.
	#
	# Called after the Update is finished, to push all buffers.
	def _PostUpdate(self):

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




## Oscillator circuit.
#
# \image html waver.png "schema"
# Creates sine and cosine waves with the specifics given by the inputs.
# Can also create a sawtooth wave and a linear increasing signal (Ramper)
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:
# 	- \f$amp\f$ amplitude
# 	- \f$freq\f$ frequency
# 	- \f$offset\f$ offset value
#	- \f$speed\f$ The rate at which the ramper will increase 
#
# - Output channels:
# 	- \f$sin\f$ sine wave \f$ = amp\cdot\sin(2 \pi freq\cdot t) + offset \f$
# 	- \f$cos\f$ cosine wave \f$ = amp\cdot\cos(2 \pi freq\cdot t) + offset \f$
# 	- \f$saw\f$ sawtooth wave \f$ = amp\cdot( freq*f(t) - floor(freq*f(t) ) + offset \f$
#
# 
# \b Example:
# \code{.py}
# machine.AddCircuit(type='waver', name='wgen')
# machine.AddCircuit(type='waver', name='wgen', amp=1.2, freq=12000)
# \endcode
#
class waver(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("freq")
		self.AddInput("amp")
		self.AddInput("offset")
		self.AddInput("speed")

		self.AddOutput("sin")
		self.AddOutput("cos")
		self.AddOutput("saw")

		self.SetInputs(**keys)


		self.counter = 0

	def Initialize (self):

		pass




	def Update (self):

		phase = self.machine.time * self.I["freq"].value

		self.O['cos'].value = self.I['amp'].value*math.cos(phase) + self.I['offset'].value
		self.O['sin'].value = self.I['amp'].value*math.sin(phase) + self.I['offset'].value
		self.O['sawtooth'].value = self.I['amp'].value * (self.machine.time *self.I["freq"].value - math.floor(self.machine.time *self.I["freq"].value)) + self.I['offset'].value


## Output circuit.
#
# Use this to dump the values of channels in a log file. 
# The channel values that are printed to the file are added/removed using the
# RegisterChannel/Unregister functions
# The input channel 'record'
# if connected will make the circuit print to file only 
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
#
# 
# \b Example:
# \code{.py}
# logger = machine.AddCircuit(type='output', name='logger', dump=1)
# logger = machine.AddCircuit(type='output', name='logger', dump=100)
# \endcode
#
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
	#
	# @param *args Channel tags to be printed in the output.
	#
	# \b Example:
	# \code{.py}
	# logger = machine.AddCircuit(type='output', name='logger', dump=100)
	# logger.Register('global.time','waver.sin','adder.out', ...)
	# \endcode
	#
	def Register(self, *args):

		#if type(channel) is list:
		#cclist = [j.split(".",1) for j in channel]
		cclist = [self.machine.GetChannel(tag) for tag in args]
		self.channels.extend(cclist)
		#else :

		#	if not(channel in self.channels):
		#		self.channels.append(channel)


	## Unregister a channel from the output.
	#
	# If the channel is already unregistered, it won't be unregistered again.
	#
	# @param *args Channel tags to be removed from the output.
	#
	# \b Example:
	# \code{.py}
	# logger = machine.AddCircuit(type='output', name='logger', dump=100)
	# logger.RegisterChannel('global.time','waver.sin','adder.out', ...)
	# ...
	# logger.Unregister('adder.out', ...)
	# \endcode
	#
	def Unregister(self, *args):
		
		cclist = [self.machine.GetChannel(tag) for tag in args]
		cclist = [x for x in self.channels.extend if x not in cclist]

		self.channels = cclist
		
		

	def Initialize (self):

		pass




	def Update (self):


		if self.I['record'].signal.owner != self:

			#if the record channel is connected and it is positive valued
			#write to file
			if self.I['record'].value > 0:
				for i in self.channels:
					self._file.write(str(i.value)+" ")
				self._file.write('\n')

		else: #if not connected...

			#if the dumprate is 0, do not print!
			if self.dump == 0:
				return

			self._cnt += 1

			if self._cnt == self.dump:
				self._cnt = 0
				#dump the data

				for i in self.channels:
					self._file.write(str(i.value)+" ")
				self._file.write('\n')


## Average circuit.
#
# This circuit will return a running average of an input signal.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
# 	
#
# - Input channels:\n
# 	- \f$in\f$
#
# - Output channels:\n
# 	- \f$out\f$
#
class Average(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in")
		self.AddOutput("out")

		self.SetInputs(**keys)


		self.counter = 1

		self.sum = 0

	def Initialize (self):

		pass
	

	def Update (self):
		# @todo this will overflow! the average should be computed within a sample buffer!
		self.sum = self.I['in'].value + self.sum
		self.O['out'].value = self.sum / self.counter
		self.counter = self.counter + 1

## Limiter circuit.
#
# This circuit will limit a signal from going above the max and below the min values.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
# 	- min = the min threshold value
#	- max = the max threshold value
#
# - Input channels:\n
# 	- \f$in\f$
#
# - Output channels:\n
# 	- \f$out\f$
#
class Limiter(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in")
		self.AddInput("min")
		self.AddInput("max")
		self.AddOutput("out")

		self.min = 0
		self.max = 0
		
		# @todo if min/max are channels, they do not need to be initialised as parameters!
		#if 'Min' in keys.keys():
			#self.min = keys['Min']
		#else:
			#raise NameError("Missing min input!")

		#if 'Max' in keys.keys():
			#self.max = keys['Max']
		#else:
			#raise NameError("Missing max input!")


		self.SetInputs(**keys)

	def Initialize (self):

		pass




	def Update (self):
	
		self.O["out"].value =  max(min(self.I["in"].value, self.I["max"].value), 
			self.I["min"].value)


## PI circuit.
#
# This circuit will compare the input signal with a reference signal and output changes in order to minimise the difference
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
#
# - Input channels:\n
# 	- \f$signal\f$
# 	- \f$Kp\f$ Proportionality tuning constant
# 	- \f$Ki\f$ Integral tuning constant
# 	- \f$set\f$
#
# - Output channels:\n
# 	- \f$out\f$ = Enter Equation here
#
class PI(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddInput("Kp")
		self.AddInput("Ki")
		self.AddInput("set")
		self.AddOutput("out")

		self.Kp = 0
		self.Ki = 0
		self.delta = 0
		self.integral=0
		self.oldInt=0
		
		self.SetInputs(**keys)

	def Initialize (self):

		pass



	def Update (self):

		self.delta =  self.I["set"].value - self.I["signal"].value
		self.integral = self.integral + ( 0.5*(self.oldInt + self.Ki*self.delta)*self.machine.dt  )
		self.O["out"].value = self.delta * self.Kp + self.integral
		self.oldInt = self.Ki * self.delta #@todo is this correct?


## PID circuit.
#
# This circuit will compare the input signal with a reference signal and output changes in order to minimise the difference, this version includes additional derivative term.
#
# - Initialisation parameters:\n
# 	- pushed = True|False  push the output buffer immediately if True
# 	- Kp = Proportionality tuning constant
#	- Ki = Integral tuning constant
#	- Kd = Derivative tuning constant
# - Input channels:\n
# 	- \f$signal\f$
# 	- \f$set\f$
#
# - Output channels:\n
# 	- \f$out\f$ = Enter Equation here
#
#@todo correct documentation!!! it does not match how the thing works!
class PID(Circuit):
    
    
	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("signal")
		self.AddInput("Kp")
		self.AddInput("Ki")
		self.AddInput("Kd")
		self.AddInput("set")
		self.AddOutput("out")

		self.Kp = 0
		self.Ki = 0
		self.delta = 0
		self.integral=0
		self.oldInt=0
		self.olddelta = 0
		self.counter = 0

		self.SetInputs(**keys)

	def Initialize (self):

		pass




	def Update (self):
		self.delta =  self.I["set"].value - self.I["signal"].value
		self.integral = self.integral + ( 0.5*(self.oldInt + self.Ki*self.delta)*self.machine.dt  )
		if self.counter > 0:
			self.O["out"].value = self.delta * self.Kp + self.integral  + self.Kd *(self.delta-self.olddelta)/self.machine.dt
		self.oldInt = self.Ki * self.delta
		self.olddelta = self.delta
		self.counter = self.counter + 1
