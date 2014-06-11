#!/usr/bin/env python

<<<<<<< HEAD
from vafmcircuits import Machine


def main():
	
=======
from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_pycirc


def main():
	
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	machine.AddCircuit(type='waver',name='wave', amp=1, freq=1, pushed=True )
<<<<<<< HEAD
  	pyc = machine.AddCircuit(type='myCirc',name='pytest', in2=1.1, pushed=True )
	
	machine.Connect("wave.sin","pytest.in1")

	out1 = machine.AddCircuit(type='output',name='output',file='test_pycircuit.out', dump=1)
=======
  	pyc = machine.AddCircuit(type='myCirc',name='pytest', pushed=True )
	
	
	machine.Connect("wave.sin","pytest.in")

	out1 = machine.AddCircuit(type='output',name='output',file='test_pycircuit.log', dump=1)
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	out1.Register('global.time', 'wave.sin', 'pytest.out')
	
	machine.Wait(1)

<<<<<<< HEAD
=======
	
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d

if __name__ == '__main__':
	main()

