#!/usr/bin/env python
<<<<<<< HEAD

from vafmcircuits import Machine


def main():
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	#Add Circuits
=======
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_avg
import vafmcircuits_math


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
  	machine.AddCircuit(type='waver',name='osc', amp=1, freq=1, pushed=True )
	machine.AddCircuit(type='avg', name='avg', time=10, pushed=True)
	machine.AddCircuit(type='avg', name='avg2', time=1, moving=True, pushed=True)
  	
	machine.Connect("osc.sin","avg.signal","avg2.signal")

<<<<<<< HEAD
	out1 = machine.AddCircuit(type='output',name='output',file='test_avg.out', dump=2)
	out1.Register('global.time', 'osc.sin', 'avg.out','avg2.out')
	
	machine.Wait(10)
=======
	out1 = machine.AddCircuit(type='output',name='output',file='test_avg.dat', dump=2)
	out1.Register('global.time', 'osc.sin', 'avg.out','avg2.out')
	
	machine.Wait(10)

>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	

if __name__ == '__main__':
	main()

