import abc
import itertools
import inspect
import sys
from collections import OrderedDict

import vafmbase

import vafmcircuits
import vafmcircuits_math

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
		
		self.O = OrderedDict()
		self.O['time'] = vafmbase.Channel('time',self,False)
		
		pass
	
	## Total simulation time.
	@property
	def time(self):
		return self._idt*self.dt
	
	## Add a circuit of type 'ctype' named 'name' to the setup.
	#
	# This looks into all the loaded modules whose name starts with
	# 'vafmcircuits' and finds the first class named 'ctype'. 
	# It then instantiate the class.
	# @param ctype Name of the class of the circuit to add.
	# @param name Name of the circuit in the setup.
	# @param **argkw Keyworded arguments for circuit initialisation.
	# @return Reference to the created circuit.
	def AddCircuit(self, ctype, name, **argkw):
		
		lst = sys.modules.keys()
		classobj = None
		
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
		if name in self.circuits.keys():
			raise NameError("A circuit named '"+name+"' already exists in the setup!")
		
		#instantiate
		instance = classobj[1](machine=self, name=name, **argkw)
		self.circuits[name] = instance
		
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
	




