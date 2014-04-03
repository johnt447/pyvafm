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
	machine.AddCircuit(type='opAdd',name='add'+str(0), amp=1, pushed=True)
	machine.Connect("wave.sin","add0.in1")
	machine.Connect("wave.cos","add0.in2")
	
	for i in range(1,10):
		machine.AddCircuit(type='opAdd',name='add'+str(i), amp=1, pushed=True)
		machine.Connect("wave.sin","add"+str(i)+".in1")
		machine.Connect("add"+str(i-1)+".out","add"+str(i)+".in2")
				   
	for i in range(10000000):
		machine.Update()
		
	

if __name__ == '__main__':
	main()

