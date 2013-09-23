#!/usr/bin/env python

import vafmcore


def main():
	
	
	machine = vafmcore.VAFM();

        
	
	machine.AddCircuit(type='opSub',name='diff', pushed=True, in1=3)
	machine.AddCircuit(type='opAdd',name='adder1', pushed=True)
	machine.AddCircuit(type='opMul',name='mult1')
	out1 = machine.AddCircuit(type='output',name='out1', file='log.log', dump=1)
	
	machine.AddCircuit(type='waver',name='wave', freq=10, amp=1)
	
	out1.RegisterChannel(['machine.time', 'wave.sin', 'wave.cos','adder1.out','diff.out'])
	
	machine.Initialize()
	
	machine.Connects("wave.sin","adder1.in1","diff.in1")
	machine.Connect("wave.cos","adder1.in2")
	machine.Connects("wave.cos","adder1.in2","diff.in2")
	
	for i in range(100):
		#print machine.time, machine.circuits['wave'].O['cos'].value
		machine.Update()
	machine.Disconnect("adder1.in1")
	for i in range(100):
		machine.Update()	


if __name__ == '__main__':
	main()
