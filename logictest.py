#!/usr/bin/env python

import vafmcore


def main():
	
	
	machine = vafmcore.VAFM();
	#Add Circuits
  	machine.AddCircuit(type='integral',name='sinint', pushed=True )
  	machine.AddCircuit(type='integral',name='cosint', pushed=True )
	out1 = machine.AddCircuit(type='output',name='out1', file='log.dat', dump=1)
	machine.AddCircuit(type='waver',name='wave', freq=1, amp=1)
	
	out1.RegisterChannel(['machine.time', 'wave.sin', 'sinint.out','wave.cos', 'cosint.out'])
	

	machine.Initialize()
	

	#Connections
	machine.Connect("wave.sin","sinint.in")
	machine.Connect("wave.cos","cosint.in")

	#machine.Connect("wave.sin","And.in2")

	

	#total time here is 2s
	for i in range(3000):
		#print machine.time, machine.circuits['wave'].O['cos'].value
		machine.Update()	


if __name__ == '__main__':
	main()
