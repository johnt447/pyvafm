<<<<<<< HEAD
#!/usr/bin/env python

from vafmcircuits import Machine

=======
##!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/pyvafm-master/src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
#test
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d

def main():
	
	#main machine
	machine = Machine(name='machine', dt=0.0001, pushed=True);
	
	# wave generator
	machine.AddCircuit(type='waver',name='wave', amp=1, freq=2, phi=1, offset=2.0, pushed=True)
	machine.AddCircuit(type='square',name='sqw', amp=1.5, freq=2, offset=0.0, duty=0.2, pushed=True )
	
	#output to file - dump=0 means only manual dump
<<<<<<< HEAD
	out1 = machine.AddCircuit(type='output',name='output',file='test_wavers.out', dump=1)
=======
	out1 = machine.AddCircuit(type='output',name='output',file='test_wavers.log', dump=1)
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	out1.Register('global.time', 'wave.sin', 'wave.cos', 'wave.saw', 'sqw.out')
	
	
	machine.Wait(1)
	
<<<<<<< HEAD
=======
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d

if __name__ == '__main__':
	main()

