#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_control
import vafmcircuits_math
import vafmcircuits_Filters


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
		
  	machine.AddCircuit(type='waver',name='osc', freq=1, pushed=True)
  	machine.AddCircuit(type='OpAbs',name='abs', pushed=True)
  	machine.AddCircuit(type='ActiveLowPass',name='lp', fcut=0.02, pushed=True)
  	
	machine.AddCircuit(type='PID', name='pi', set=1,Kp=1.0,Ki=0.1,Kd=0.01)
  	
	machine.Connect("lp.out","pi.signal")
	machine.Connect("pi.out","osc.amp")
	
	machine.Connect("osc.sin","abs.in")
	machine.Connect("abs.out","lp.in")

	out1 = machine.AddCircuit(type='output',name='output',file='log.log', dump=50)
	out1.Register('global.time', 'osc.sin', 'lp.out', 'pi.out')
	
	for i in range(100000):
		machine.Update()

	

if __name__ == '__main__':
	main()

