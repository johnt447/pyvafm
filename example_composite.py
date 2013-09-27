#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_math


def ADC(compo):
	
  	compo.AddInput("signal1")
  	compo.AddInput("signal2")
  	compo.AddOutput("out")
  	compo.AddCircuit(type='opAdd',name='adder',factors=2, pushed=True)
  	compo.Connect("global.signal1","adder.in1")
  	compo.Connect("global.signal2","adder.in2")
  	compo.Connect("adder.out","global.out")
	
	print "ADC assembled!"

def main():
	
	
	machine = Machine(machine=None, name='machine', pushed=True);
	
	
	#Add Circuits
	
	
  	machine.AddCircuit(type='waver',name='osc', amp=1, freq=1, pushed=True )
  	
  	compo1 = machine.AddCircuit(type='Machine', name='compo1', assembly=ADC, pushed=True)
  	
	machine.Connect("osc.sin","compo1.signal1")
	machine.Connect("osc.cos","compo1.signal2")

	out1 = machine.AddCircuit(type='output',name='output',file='log.log', dump=1)
	out1.RegisterChannel('global.time', 'osc.sin', 'osc.cos', 'compo1.out')
	
	for i in range(1000):
		machine.Update()
		#print machine.GetChannel('global.time')

	

if __name__ == '__main__':
	main()
