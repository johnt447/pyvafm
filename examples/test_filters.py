# -*- coding:utf-8 -*-

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_signal_processing
import vafmcircuits_Filters

def main():
	
	#main machine
	machine = Machine(name='machine', dt=0.0001, pushed=True);
	
	# wave generator
	machine.AddCircuit(type='waver',name='wave', amp=1, pushed=True )
	
	#lowpass filter at fc=100
	machine.AddCircuit(type='SKLP',name='alp100', fcut=100, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='amp100', CheckTime=0.2, pushed=True)
	
	#lowpass filter at fc=200
	machine.AddCircuit(type='SKLP',name='alp200', fcut=200, pushed=True )
	#amplitude detector for the filter
	machine.AddCircuit(type='minmax', name='amp200', CheckTime=0.2, pushed=True)

	#connect oscillator to the filters
	machine.Connect("wave.sin","alp100.signal","alp200.signal")
	machine.Connect("alp100.out","amp100.signal") #filter -> amplitude detector
	machine.Connect("alp200.out","amp200.signal") #filter -> amplitude detector
	
	#output to file - dump=0 means only manual dump
	out1 = machine.AddCircuit(type='output',name='output',file='test_filters.log', dump=0)
	out1.Register('wave.freq', 'amp100.amp', 'amp200.amp')
	
	
	#set the frequency and relax the filter
	freq = 5
	machine.SetInput(channel="wave.freq", value=freq)
	machine.Wait(1)
	
	while freq < 1000:
	
		#assign the frequency to the oscillator
		machine.SetInput(channel="wave.freq", value=freq)
		
		#wait some time to charge the capacitors in the filters
		machine.Wait(1)
		
		out1.Dump() #output to file
		freq *= 1.2 #ramp the frequency
		
	

if __name__ == '__main__':
	main()

