#!/usr/bin/env python

<<<<<<< HEAD
from vafmcircuits import Machine

=======
from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits

>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d

def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	wave = machine.AddCircuit(type='waver',name='wave', amp=1, freq=2, pushed=True )
<<<<<<< HEAD
	outer= machine.AddCircuit(type='output', name='outer', file='test_output.out', dump=0 )
	outer.Register('global.time', 'wave.sin')

	machine.Connect('wave.sin','outer.record')
	
=======
	outer= machine.AddCircuit(type='output', name='outer', file='test_output.dat', dump=1 )
	outer.Register('global.time', 'wave.sin')

	#machine.Connect('wave.sin','outer.record')
	machine.SetInput(channel="outer.record", value=0)
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	machine.Wait(1)


if __name__ == '__main__':
	main()

