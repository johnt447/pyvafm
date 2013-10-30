#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_control
import vafmcircuits_math
import vafmcircuits_Filters
from customs_pll import *


def main():
	
	
	machine = Machine(name='machine', dt=1.0e-8, pushed=True);
	
	machine.AddCircuit(type='waver',name='osc', amp=1, freq=1.0e5+4, pushed=True)
	machine.AddCircuit(type="Machine",name='pll', assembly=aPLL, filters=[1000,500],
		gain=600.0, f0=1.0e5, Kp=0.4, Ki=500, pushed=True)
	
  	
	machine.Connect("osc.cos","pll.signal1")
	machine.Connect("pll.sin","pll.signal2")
	
	
	out1 = machine.AddCircuit(type='output',name='output',file='log.log', dump=10000)
	out1.Register('global.time', 'pll.signal1', 'pll.signal2', 'pll.df')
	
	for i in range(1000000):
		machine.Update()

	

if __name__ == '__main__':
	main()

