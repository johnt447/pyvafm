from vafmbase import Circuit
import math
import io


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
	def RegisterChannel(self, channel):
		
		#if type(channel) is list:
		cclist = [j.split(".",1) for j in channel]
		cclist = [self.machine.GetChannel(j[0], j[1]) for j in cclist]
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


