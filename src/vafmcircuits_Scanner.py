# -*- coding:utf-8 -*-
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine
from ctypes import *

class Scanner(Circuit):

	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		self.AddOutput("x")
		self.AddOutput("y")
		self.AddOutput("z")
		self.AddOutput("record")

		self.fastscan = [1,0,0]
		self.slowscan = [0,1,0]
		self.landscan = [0,0,1]
		self.imagesize = [1,1]
		self.resolution = [20,7]
		
		self.cCoreID = Circuit.cCore.Scanner( self.machine.cCoreID )
		self.SetInputs(**keys)


	def Move(self, x = 0, y = 0, z = 0, v = 1): #default arguments, make the input lighter
		steps = Circuit.cCore.Scanner_Move(self.cCoreID, c_double(x), c_double(y) ,c_double(z),c_double(v) )
		Machine.main.WaitSteps(steps)
		print "Scanner moved by " +str(x) + "," + str(y)+ "," + str(z)

	def Place(self,x,y,z): #all parameters required
		
		steps = Circuit.cCore.Scanner_Place(self.cCoreID, c_double(x), c_double(y), c_double(z) )
		Machine.main.WaitSteps(1)
		print "Scanner Placed at " +str(x) + "," + str(y)+ "," + str(z)

	def MoveTo(self,**kw):
		
		#finds out where the scanner is by asking cCore
		func = Circuit.cCore.ScannerParams;
		func.restype = POINTER(c_double);
		params = Circuit.cCore.ScannerParams(self.cCoreID);
		x = params[0]
		y = params[1]
		z = params[2]
		v = 0
		
		if "x" in kw.keys(): x = float(kw["x"])
		if "y" in kw.keys(): y = float(kw["y"])
		if "z" in kw.keys(): z = float(kw["z"])
		if not("z" in kw.keys()):
			v = float(kw["v"])
		else:
			raise NameError ("ERROR! Scanner MoveTo requires v.")

		steps = Circuit.cCore.Scanner_MoveTo(self.cCoreID, c_double(x), c_double(y), c_double(z), c_double(v))
		Machine.main.Wait(steps*self.machine.dt)                
		print "Scanner moved to " +str(x) + "," + str(y)+ "," + str(z)

	def Scan(self,x,y,z,v,points):
		steps = Circuit.cCore.Scanner_Scan(self.cCoreID, c_double(x), c_double(y) ,c_double(z),c_double(v),points )
		Machine.main.Wait(steps*self.machine.dt)                
		print "Scanner scanned to " +str(x) + "," + str(y)+ "," + str(z)

	## Used to set the fast scan direction
	def FastScan(self, direction):
		
		x = direction[0]
		y = direction[0]
		z = direction[0]
		n = math.sqrt(x*x + y*y + z*z)
		self.fastscan[0] = x/n
		self.fastscan[1] = y/n
		self.fastscan[2] = z/n
	
	## Used to set the slow scan direction
	def SlowScan(self, direction):
		
		x = direction[0]
		y = direction[0]
		z = direction[0]
		n = math.sqrt(x*x + y*y + z*z)
		self.slowscan[0] = x/n
		self.slowscan[1] = y/n
		self.slowscan[2] = z/n

	## Set the size of the image along the fast and slow scan directions
	def ImageArea(self, fast, slow):
		
		self.imagesize[0] = fast
		self.imagesize[1] = slow

	def ScanArea(self, v):
		
		#move to the end of fast scanline
		
		#move to initial pos + step along slowscan
		
		#repeat resolution[1] times
		
		
		
		pass




