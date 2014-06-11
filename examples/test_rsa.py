#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_rsa
from customs_pll import *

'''
center of mass position: (x,y,z) = (0, 0, 0.022m)
total mass: 0.0255kg
moment of inertia : 4.62e-6 kgm^2
positions of the springs attached :
 (x,y,z) = (-0.0141m, 0, 0.0249m) and (0.0141m, 0, 0.0249m) 
'''

def main():
	
	f0 = 30
	
	machine = Machine(name='machine', dt=1.0e-5, pushed=True);
	
	scan= machine.AddCircuit(type='Scanner', name='scan', pushed=True)
	exc = machine.AddCircuit(type='waver',name='exc', amp=1, freq=f0, pushed=True)
	
	rsa = machine.AddCircuit(type='RSA', name='rsa', eta=0.1, pushed=True)
<<<<<<< HEAD
	rsa.SetSprings(860,1500000,7000)
=======
	rsa.SetSprings(860,15000,7000)
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	rsa.SetPoints(0.0141,0.0029,-0.022)
	rsa.SetGammas(0.066, 0.2, 0.1)
	rsa.SetMasses(0.0255, 0.06, 4.62e-6)
	
<<<<<<< HEAD
	machine.AddCircuit(type='Machine', name='amp', assembly=aAMPD, fcut=4, pushed=True)
	machine.AddCircuit(type='Machine', name='ampang', assembly=aAMPD, fcut=4, pushed=True)
	machine.AddCircuit(type='Machine', name='amplow', assembly=aAMPD, fcut=1, pushed=True)
	machine.AddCircuit(type='phasor', name='philow')
	machine.AddCircuit(type='phasor', name='phitoplow')
	machine.AddCircuit(type='phasor', name='phitop')
	machine.AddCircuit(type='phasor', name='phiang')
=======
	
	
	machine.AddCircuit(type='Machine', name='amp', assembly=aAMPD, fcut=4, pushed=True)
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
 	
 	machine.Connect("scan.x","exc.freq")
 	machine.Connect("scan.y","exc.amp")
 	machine.Connect("scan.z","rsa.eta")
	machine.Connect("exc.cos","rsa.exciter")
	machine.Connect("rsa.xcm","amp.signal")
<<<<<<< HEAD
	machine.Connect("rsa.x2","amplow.signal")
	machine.Connect("rsa.theta","ampang.signal")
	machine.Connect("exc.cos","philow.in1")
	machine.Connect("rsa.x2","philow.in2")
	machine.Connect("rsa.xcm","phitoplow.in1")
	machine.Connect("rsa.x2","phitoplow.in2")
	machine.Connect("exc.cos","phitop.in1")
	machine.Connect("rsa.xcm","phitop.in2")
	machine.Connect("exc.cos","phiang.in1")
	machine.Connect("rsa.theta","phiang.in2")
	
	out1 = machine.AddCircuit(type='output',name='output',file='rsa_0.1.out', dump=1)
	out1.Register('global.time','exc.cos','rsa.xcm','rsa.x2','rsa.theta')
	out1.Stop()
=======
	
	
	#out1 = machine.AddCircuit(type='output',name='output',file='test_rsa.log', dump=4)
	#out1.Register('global.time','exc.cos')

>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d

	scan.Place(x=30,y=1,z=0.0)
	machine.Wait(2.0)
	
<<<<<<< HEAD
	eta=100.1
	out2 = machine.AddCircuit(type='output',name='res',file='rsaamp_'+str(eta)+'.out', dump=5000)
	out2.Register('exc.freq', 'amp.amp', 'amplow.amp','ampang.amp','philow.delay','phitoplow.delay','phitop.delay','phiang.delay')
	#out2.Stop()
	
	#for eta in [0.0, 0.1,  1.0, 10]:
	#for frq in [36,38,40,42,44,46,48,50,52,54,56]:
		
	scan.Place(x=36,y=1,z=eta)
	machine.Wait(5.0)
	out2.Start()
	scan.MoveTo(x=60, v=0.1)
	
	
	#out1.Start()
	#machine.Wait(5.0/frq)
	#out1.Stop()
=======
	out2 = machine.AddCircuit(type='output',name='res',file='test_rsa2.log', dump=1000)
	out2.Register('exc.freq', 'amp.amp')	
	
	for eta in [0.0, 0.1, 0.5, 1.0]:
		out2.Stop()
		scan.Place(x=30,y=1,z=eta)
		machine.Wait(2.0)
		out2.Start()
		scan.MoveTo(x=80, v=0.1)
	
>>>>>>> 72dc09fb8affb9761e7d26360f54c6668336189d
	
	
	
if __name__ == '__main__':
	main()

