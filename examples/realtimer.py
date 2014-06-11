#!/usr/bin/env python
#Mandatory Imports

from vafmbase import ChannelType
from vafmcircuits import Machine
import vafmcircuits
import subprocess

#User defined inports
import vafmcircuits_Filters


def main():

	
	machine = Machine(machine=None, name='machine', dt=0.01, pushed=False);

	
	#Add Circuits
	machine.AddCircuit(type='waver',name='wave', amp=0.5, freq=10, pushed = False)
	machine.AddCircuit(type='opAdd', name='add', pushed = False)


	#Connections
 	machine.Connect("wave.sin","add.in1")
 	machine.Connect("wave.cos","add.in2")

 	#Outputs
 	out1 = machine.AddCircuit(type='output',name='output',file='log.dat', dump=1)
	out1.Register('global.time', 'wave.sin', 'wave.sin', 'add.out')
	out1.Plot(sizex=5, sizey = 3, RealTime = True)


	machine.Wait(2)
	

	#out1.FinishPlot()

if __name__ == '__main__':
	main()
