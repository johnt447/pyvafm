from vafmbase import Circuit
import math

class GreaterOrEqual(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value >= self.I["in2"].value :
			result=1
		self.O['out'].value = result

class LessOrEqual(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value <= self.I["in2"].value :
			result=1
		self.O['out'].value = result


class Equal(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )

		self.AddInput("in1")
		self.AddInput("in2")

		self.AddOutput("out")

		self.SetInputs(**keys)

	def Initialize (self):

		pass	

	def Update (self):
		result=0

		if self.I["in1"].value == self.I["in2"].value :
			result=1
		self.O['out'].value = result