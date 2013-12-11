
from ctypes import *
import threading




testlib = cdll.LoadLibrary("./vafmcore.so")
print testlib

#calls the function in the library
testlib.INIT()

widx = testlib.Add_waver()
testlib.SetInput(widx,0,c_double(2.0))
testlib.SetInput(widx,1,c_double(1.0))
testlib.SetInput(widx,2,c_double(1.0))
#testlib.DebugCircuit(widx)

andidx = testlib.Add_Logic("opOR",2)
addidx = testlib.Add_Math("opADD",2)
#testlib.DebugCircuit(andidx)

testlib.Connect(widx,0,andidx,0)
testlib.Connect(widx,1,andidx,1)



outidx = testlib.Add_output("log.log",2);
testlib.output_register(outidx,-1,0)
testlib.output_register(outidx,widx,0)
testlib.output_register(outidx,widx,1)
testlib.output_register(outidx,andidx,0)

#testlib.DebugCircuit(outidx)

testlib.Update(10000)

#testlib.DebugCircuit(widx)
"""
for i in range(10):
    idx = testlib.AddCircuit("opADD",2,1)
    testlib.Connect(0,i%2,idx,1)
    testlib.Connect(idx-1,1,idx,0)

#outidx = testlib.Add_output("log.log",2);
#testlib.output_register(outidx,-1,0)
#testlib.output_register(outidx,widx,0)
#testlib.output_register(outidx,widx,1)
#testlib.output_register(outidx,widx+1,0)

#testlib.DebugCircuit(outidx)

#testlib.Status()
t = threading.Thread(target=testlib.Update, args=[100000000])
t.daemon = True
t.start()
while t.is_alive(): # wait for the thread to exit
    t.join(.1)

#testlib.output_close(outidx);

#print testlib.SUM()
"""



