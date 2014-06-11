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
  	machine.AddCircuit(type='waver',name='osc', amp=0.2, freq=1.3, pushed=True )
	machine.AddCircuit(type='peaker', name='pkd', up=True, pushed=True)
	
	machine.Connect("osc.sin","pkd.signal")

<<<<<<< HEAD
	out1 = machine.AddCircuit(type='output',name='output',file='test_peaker.out', dump=1)
	out1.Register('global.time', "osc.sin","pkd.tick","pkd.peak","pkd.delay")
	
	machine.Wait(5)
=======
	out1 = machine.AddCircuit(type='output',name='output',file='test_peaker.log', dump=1)
	out1.Register('global.time', "osc.sin","pkd.tick","pkd.peak","pkd.delay")
	
	machine.Wait(5)

>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	

if __name__ == '__main__':
	main()

