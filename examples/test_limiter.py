#!/usr/bin/env python

<<<<<<< HEAD
from vafmcircuits import Machine


def main():
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
=======
from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_signal_processing


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	#Add the circuits	
  	machine.AddCircuit(type='waver',name='osc', amp=1, freq=1.3, pushed=True )
	machine.AddCircuit(type='limiter', name='lim', max=0.7, min=-0.3, pushed=True)
	
	machine.Connect("osc.sin","lim.signal")

<<<<<<< HEAD
	out1 = machine.AddCircuit(type='output',name='output',file='test_limiter.out', dump=1)
=======
	out1 = machine.AddCircuit(type='output',name='output',file='test_limiter.log', dump=1)
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	out1.Register('global.time', "osc.sin","lim.out")
	
	machine.Wait(5)

<<<<<<< HEAD
=======
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d

if __name__ == '__main__':
	main()

