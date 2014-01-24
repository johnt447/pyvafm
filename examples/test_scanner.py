#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_signal_processing
import vafmcircuits_Scanner


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	scanner = machine.AddCircuit(type='Scanner',name='scan', pushed=True )
  	
	
	out1 = machine.AddCircuit(type='output',name='output',file='test_scanner.log', dump=1)
	out1.Register('global.time', "scan.x", "scan.y", "scan.z")
	out2 = machine.AddCircuit(type='output',name='image',file='test_scanner_image.log', dump=0)
	out2.Register('global.time', "scan.x", "scan.y")
	
	machine.Connect("scan.record","image.record")
	
	#machine.Wait(10)
	scanner.Move(0.5,1,0,1)
	scanner.Move(0.5,-0.5,-0.2,1)
	scanner.Place(0,0.1,0.2)
	scanner.MoveTo(x=1, v=1)
	
	
	#machine.Wait(0.1)
	

if __name__ == '__main__':
	main()

