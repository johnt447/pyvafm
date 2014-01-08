/**********************************************************
Filters circuits definitions.
 *********************************************************/
#include <math.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREFILTERS
#include "core_filters.h"
#endif



void INIT_FILTERS(int* counter) {

    int i = *counter;
    

    pynames[i] = "SKLP"; ufunctions[i] = SKLP; i++;

    
    *counter = i;

}

/*********************************************************
 * Sallen-Key lowpass filter.
 * params[0] fcut
 * params[1] Q
 * params[2] gain
 * params[3] wc
 * params[4] gamma
 * params[5] alpha
 * params[6] yo
 * params[7] yoo
 * ******************************************************/
int Add_SKLP(int owner, double fcut, double Q, double gain) {
	
	circuit c = NewCircuit();
	c.nI = 1;
	c.nO = 1;
	
	c.plen = 8;
	c.params = (double*)calloc(c.plen,sizeof(double));
	
	double wc = fcut * 2 * PI * dt;
	double gamma = wc / (2*Q);
	wc = wc * wc;
	double alpha = 1.0/(1.0+gamma+wc);
	
	c.params[0] = fcut;
	c.params[1] = Q;
	c.params[2] = gain;
	c.params[3] = wc;
	c.params[4] = gamma;
	c.params[5] = alpha;
	c.params[6] = 0;
	c.params[7] = 0;
	
	c.updatef = ufunctions[GetCircuitIndex("SKLP")];
	
	int index = AddToCircuits(c,owner);
	printf("added SKLP filter\n");
	return index;
}

void SKLP( circuit *c ) {
	
	double v = GlobalSignals[c->inputs[0]];
	//printf("filtered1\n");
	v = c->params[2]*c->params[3]*v + (2.0*c->params[6]-c->params[7]) + c->params[4]*c->params[7];
	v = v * c->params[5];
	GlobalBuffers[c->outputs[0]] = v;

	c->params[7] = c->params[6];
	c->params[6] = v;
	
}

