#!/usr/bin/env python

<<<<<<< HEAD
from vafmcircuits import Machine


def main():
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	#Add Circuits
=======
from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits

import vafmcircuits_signal_processing


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
  	machine.AddCircuit(type='waver',name='osc', amp=1, freq=1, pushed=True )
	machine.AddCircuit(type='derivative', name='der', pushed=True)
	machine.AddCircuit(type='integral', name='int', pushed=True)
	
<<<<<<< HEAD
	machine.Connect("osc.sin","der.signal","int.signal")

	out1 = machine.AddCircuit(type='output',name='output',file='test_derint.out', dump=2)
	out1.Register('global.time', 'osc.sin', 'osc.cos','der.out','int.out')
	
	machine.Wait(10)
=======
  	
	machine.Connect("osc.sin","der.signal","int.signal")

	out1 = machine.AddCircuit(type='output',name='output',file='test_derint.log', dump=2)
	out1.Register('global.time', 'osc.sin', 'osc.cos','der.out','int.out')
	
	machine.Wait(10)

>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	

if __name__ == '__main__':
	main()

