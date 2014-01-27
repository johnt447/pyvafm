/**********************************************************
Flip-Flop circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREFLIPFLOP
#include "core_flipflops.h"
#endif


int Add_DRFlipFLop(int owner) {

    circuit c = NewCircuit();
    c.nI = 2;
    c.nO = 2;
    
    c.plen = 2;
    c.params = (double*)calloc(c.plen,sizeof(double));

    c.updatef = DRFlipFlop;
    
    int index = AddToCircuits(c,owner);
    printf("cCore: added DRFlipFlop circuit\n");
    return index;
    
}

void DRFlipFlop( circuit *c ) {
	
	double D = GlobalSignals[c->inputs[0]];
	double R = GlobalSignals[c->inputs[1]];
	double Qprevious = c->params[0];

	if (D<= 0 && Qprevious <= 0)
	{

		GlobalBuffers[c->outputs[0]] = 0;
		GlobalBuffers[c->outputs[1]] = 1;
	}

	if (D<= 0 && Qprevious > 0)
	{
		GlobalBuffers[c->outputs[0]] = 0;
		GlobalBuffers[c->outputs[1]] = 1;
  
	}

	if (D > 0 && Qprevious <= 0)
	{
		GlobalBuffers[c->outputs[0]] = 1;
		GlobalBuffers[c->outputs[1]] = 0;

	}

	if (D > 0 && Qprevious > 0)
	{
		GlobalBuffers[c->outputs[0]] = 1;
		GlobalBuffers[c->outputs[1]] = 0;

	}

	if (R > 0)
	{
		GlobalBuffers[c->outputs[0]] = 0;
		GlobalBuffers[c->outputs[1]] = 1;
   
	}

	Qprevious = GlobalBuffers[c->outputs[0]];
	c->params[0] = Qprevious;

}
