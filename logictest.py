#!/usr/bin/env python

import vafmcore


def main():
	
	
	machine = vafmcore.VAFM();
	#Add Circuits
  	machine.AddCircuit(type='OpPower',name='And', pushed=True, power=2)
	out1 = machine.AddCircuit(type='output',name='out1', file='log.dat', dump=1)
	machine.AddCircuit(type='waver',name='wave', freq=10, amp=1)
	
	out1.RegisterChannel(['machine.time', 'And.out', 'wave.cos', 'wave.sin'])
	

	machine.Initialize()
	

	#Connections
	machine.Connect("wave.cos","And.in")
	#machine.Connect("wave.sin","And.in2")
	
	for i in range(100):
		#print machine.time, machine.circuits['wave'].O['cos'].value
		machine.Update()

	for i in range(100):
		machine.Update()	


if __name__ == '__main__':
	main()
