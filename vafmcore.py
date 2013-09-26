import abc
import itertools
import inspect
import sys
from collections import OrderedDict

import vafmbase

import vafmcircuits
import vafmcircuits_math
import vafmcircuits_Logic
import vafmcircuits_signal_processing
import vafmcircuits_composite

## Virtual Machine class.
#
class VAFM(object):
	
	
	
	def __init__(self):
		
		## Ordered dictionary of the circuits in the setup.
		self.circuits = OrderedDict()
		## Integration timestep
		self.dt = 1.0e-2
		## Integer number of update steps so far.
		self._idt = 0;
		
		## Dictionary of input channels
		self.I = {}
		## Dictionary of output channels
		self.O = {}
		
		#self.O = OrderedDict()
		self.O['time'] = vafmbase.Channel('time',self,False)
		
		
	
	## Total simulation time.
	@property
	def time(self):
		return self._idt*self.dt
	

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
	
	## Find a channel given its name and the name of the circuit.
	# @param cname Name of the circuit.
	# @param chname Name of the channel to find.
	# @return Reference to the channel.
	def GetChannel(self, cname, chname):
		
		if cname == 'machine':
			return self.O[chname]
		
		if not(cname in self.circuits.keys()):
			raise NameError( "GetChannel error: circuit "+cname+" not found." )
		
		return self.circuits[cname].GetChannel(chname)
	
	## (deprecated) Connect the output of a circuit to the input of another.
	# The I/O channels to connect are specified with the syntax: "circuit.channel"
        # @param O Name of the output channel (source signal) given as string: "circuit.channel"
        # @param I Name of the input channel (destination) given as string: "circuit.channel"
	def Connect(self, O, I):
		
		onames = O.split(".",1)
		inames = I.split(".",1)
		
		print "connecting " + O + " -> " + I
		
		#check existence of circuits
		if not(onames[0] in self.circuits.keys()):
			raise NameError( "Connection error: circuit "+onames[0]+" not found." )
		if not(inames[0] in self.circuits.keys()):
			raise NameError( "Connection error: circuit "+inames[0]+" not found." )
		
		#check existence of channels
		if not(onames[1] in self.circuits[onames[0]].O.keys()):
			raise NameError( "Connection error: channel "+onames[1]+" not found." )
		if not(inames[1] in self.circuits[inames[0]].I.keys()):
			raise NameError( "Connection error: channel "+inames[1]+" not found." )
		
		self.circuits[inames[0]].I[inames[1]].signal = self.circuits[onames[0]].O[onames[1]].signal

	## Connect the output of a circuit to the input of another.
	# The I/O channels to connect are specified with the syntax: "circuit.channel", in the *args arguments
	# array. The first element has to be the output channel to use as source, while all
	# the following elements refer to the destination channels.
        # @param *args Name of the channels to connect: "circuit.channel"
	def Connects(self, *args):
		
		onames = args[0].split(".",1)

		#check existence of output circuit.channel
		if not(onames[0] in self.circuits.keys()):
			raise NameError( "Connection error: circuit "+onames[0]+" not found." )

                print "connecting " + args[0]
                
                for i in args[1:]:

                    inames = i.split(".",1)

                    #check existence of channels
                    if not(inames[1] in self.circuits[inames[0]].I.keys()):
			raise NameError( "Connection error: channel "+inames[1]+" not found." )

		    print "  -> " + i
		    self.circuits[inames[0]].I[inames[1]].signal = self.circuits[onames[0]].O[onames[1]].signal

                    
	
	## (deprecated) Disconnect an input channel.
	# This is achieved by renewing the Feed object in the channel. If the channel was
	# not connected, it does not really matter.
	# The input channel to disconnect is specified with the syntax: "circuit.channel"
        # @param I Name of the input channel given as string: "circuit.channel"
	def Disconnect(self, I):
		
		inames = I.split(".",1)
		
		print "disconnecting " + I
		
		#check existence of circuit
		if not(inames[0] in self.circuits.keys()):
			raise NameError( "Disconnection error: circuit "+inames[0]+" not found." )
		
		#check existence of channels
		if not(inames[1] in self.circuits[inames[0]].I.keys()):
			raise NameError( "Connection error: input channel "+inames[1]+" not found." )
		
		self.circuits[inames[0]].I[inames[1]].Disconnect()

	## Disconnect a group of input channels.
	# This is the same as Disconnect, but it can take multiple "circuit.channel" arguments.
        # @param *args Input channels given as list of strings of format: "circuit.channel"
	def Disconnects(self, *args):

                print "disconnecting: "
		for i in args:

        		inames = i.split(".",1)	

                        #check existence of circuit
                        if not(inames[0] in self.circuits.keys()):
                            raise NameError( "Disconnection error: circuit "+inames[0]+" not found." )
		
                        #check existence of channels
                        if not(inames[1] in self.circuits[inames[0]].I.keys()):
                            raise NameError( "Connection error: input channel "+inames+" not found." )
		
                        print "  - "+ inames
                        self.circuits[inames[0]].I[inames[1]].Disconnect()
                        
		
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
		
		for kw in self.circuits.keys():
			
			self.circuits[kw].Update()
			
			if self.circuits[kw].pushed: #push if needed
				self.circuits[kw].Push()
		
		self._idt += 1
		self.O['time'].Set(self.time)
		
		self.PostUpdate()
	
	## Post Update cycle.
	#
	# Called after the Update is finished, to push all buffers.
	def PostUpdate(self):
		
		for kw in self.circuits.keys():
			self.circuits[kw].Push()




