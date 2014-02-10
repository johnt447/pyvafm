#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine


def main():

        
        machine = Machine(machine=None, name='machine', dt=0.01)
	
        scan = machine.AddCircuit(type='Scanner',name='scann', pushed=True)
        inter = machine.AddCircuit(type='i3Dlin',name='inter', components=1, pushed=True)

	machine.Connect("scann.x" , "inter.x")
	machine.Connect("scann.y" , "inter.y")
	machine.Connect("scann.z" , "inter.z")
	

        #Outputs
        out1 = machine.AddCircuit(type='output',name='output',file='test_i3Dlin.dat', dump=1)
        out1.Register('global.time', "scann.x","scann.y","scann.z",'inter.F1')
	
        #scan.Place(1,1,30)
        #scan.MoveTo(1,1,40,0.1)

	inter.Configure(steps=[0.2,0.3,0.2], npoints=[3,3,3])
	inter.Configure(pbc=[True,True,False])
	inter.ReadData('test_i3Dlin_force.dat')
	
	scan.MoveTo(x=1,v=1)
	scan.Place(x=0,z=0.1)
	scan.MoveTo(x=1,v=1)
	scan.Place(x=0,z=0.2)
	scan.MoveTo(x=1,v=1)
	

if __name__ == '__main__':
        main()
