## \file customs_pll.py
# Contain the assembly functions for composite PLL circuits.
#

from vafmbase import Circuit
from vafmcircuits import Machine
import math

import vafmcircuits_Filters
import vafmcircuits_math
import vafmcircuits_control
import vafmcircuits_signal_processing


def aPLL(compo,**keys):
	
	# I/O
  	compo.AddInput("signal1")
  	compo.AddInput("signal2")
  	compo.AddInput("f0")
  	
  	compo.AddOutput("sin")
  	compo.AddOutput("cos")
  	compo.AddOutput("df")
  	compo.AddOutput("dbg")
  	
  	
  	filters = keys['filters']
  	print "prefilters cutoffs: ",filters
  	
  	compo.AddCircuit(type='opMul',name='pfd', pushed=True)
  	for i in range(len(filters)):
		f = filters[i]
		compo.AddCircuit(type='ActiveLowPass',name='lp'+str(i+1),fcut=f, pushed=True)
		
  	compo.AddCircuit(type='Gain',name='dfgain', gain=keys['gain'], pushed=True)
  	compo.AddCircuit(type='PI',name='pump', Kp=keys['Kp'],Ki=keys['Ki'], set=0, pushed=True)
  	compo.AddCircuit(type='opAdd',name='fsum', pushed=True)
  	compo.AddCircuit(type='waver',name='vco', amp=1, pushed=True)
  	

  	
  	#connections
  	compo.Connect("global.signal1","pfd.in1")
  	compo.Connect("global.signal2","pfd.in2")
  	
  	compo.Connect("pfd.out","lp1.in")
	for i in range(1,len(filters)):
		compo.Connect("lp"+str(i)+".out","lp"+str(i+1)+".in")
  	
  	compo.Connect("lp"+str(len(filters))+".out","pump.signal")
  	compo.Connect("pump.out","dfgain.in")
  	compo.Connect("dfgain.out","fsum.in1","global.df")
  	compo.Connect("global.f0", "fsum.in2")
	compo.Connect("fsum.out",   "vco.freq")
	compo.Connect("vco.sin",   "global.sin")
	compo.Connect("vco.cos",   "global.cos")
	compo.Connect("pfd.out",   "global.dbg")
	
	#debug
	#out1 = compo.AddCircuit(type='output',name='output',file='pll.log', dump=1000)
	#out1.Register('global.time',"lp"+str(len(filters))+".out",'pump.out',"global.df")

	print "analog PLL assembled!"
