#!/usr/bin/env python

import vafmcore


def main():
	
	
	machine = vafmcore.VAFM();

	#waver = circs.Wave(machine, 'waver');
	
	#machine.circuits['waver'] = waver
	
	#print machine.circuits
	##print machine.circuits['asd']

	#waver.I['freq'].Set(1);
	#waver.I['amp'].Set(1);

	#print waver.asder
	#print str(waver)
	
	machine.AddCircuit('opAdd','adder2', factors=3, pushed=True)
	machine.AddCircuit('opAdd','adder1', pushed=True)
	machine.AddCircuit('opMul','mult1')
	out1 = machine.AddCircuit('output','out1', file='log.log', dump=1)
	
	machine.AddCircuit('waver','wave', freq=10, amp=1)
	
	out1.RegisterChannel(['machine.time', 'wave.cos', 'wave.sin','adder1.out'])
	
	machine.Initialize()
	
	machine.Connect("wave.sin","adder1.in1")
	machine.Connect("wave.cos","adder1.in2")
	
	for i in range(100):
		#print machine.time, machine.circuits['wave'].O['cos'].value
		machine.Update()
	
	

if __name__ == '__main__':
	main()
