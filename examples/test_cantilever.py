#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
from customs_pll import *


def main():
	
	
	machine = Machine(name='machine', dt=5.0e-8, pushed=True);
	
	
	#Add Circuits
	canti = machine.AddCircuit(type='Cantilever',name='canti', startingz=0,
		Q=100, k=167.0, f0=100000.0, pushed=True)
	
	machine.AddCircuit(type='Machine', name='ampd', assembly=aAMPD, fcut=10000, pushed=True)
	machine.AddCircuit(type='PI', name='AGC', Kp=10.1, Ki=10000, set=1, pushed=True)
	machine.AddCircuit(type='waver', name='wave', freq=100000.0, pushed=True)
	
	machine.Connect('canti.ztip','ampd.signal')
	machine.Connect('ampd.amp','AGC.signal')
	machine.Connect('AGC.out','wave.amp')
	machine.Connect('wave.sin','canti.exciter')
	
	#debug output
	out1 = machine.AddCircuit(type='output',name='output',file='test_cantilever.log', dump=7)
	out1.Register("global.time", "canti.ztip","ampd.amp","canti.vz")
	
	machine.Wait(0.01)

if __name__ == '__main__':
	main()


