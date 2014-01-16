# -*- coding:utf-8 -*-

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits


def main():
	
	#main machine
	machine = Machine(name='machine', dt=0.0001, pushed=True);
	
	# wave generator
	machine.AddCircuit(type='waver',name='wave', amp=1, freq=2, phi=1, offset=2.0, pushed=True )
	
	
	#output to file - dump=0 means only manual dump
	out1 = machine.AddCircuit(type='output',name='output',file='test_wavers.log', dump=1)
	out1.Register('global.time', 'wave.sin', 'wave.cos', 'wave.saw')
	
	
	machine.Wait(1)
	
	

if __name__ == '__main__':
	main()

