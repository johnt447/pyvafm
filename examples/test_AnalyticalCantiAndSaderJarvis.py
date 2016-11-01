#!/usr/bin/env python

from vafmcircuits import Machine


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	

	machine.AddCircuit(type='AnalyticalCantilever',name='AC', pushed=True, 
		filename = 'NaClforces.dat' ,
		NumberOfPoints=[8,8,201],
		step = [0.705,0.705,0.1],
		K=130,
		f0=1553e6,
		A=1,
		res = [51,51,201],
		NumberOfFFCells = [1,1,1],
		convertion =10000,
		OutputFile="NaCldf.dat",
		OscRes = 100,
		ScanType = "Vertical",
		TipPos = [0,0,3.2],
		MinMaxz = [4, 25]
		)
	
	

if __name__ == '__main__':
	main()
