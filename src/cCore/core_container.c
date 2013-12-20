/**********************************************************
Circuits container definitions.
 *********************************************************/
#include <math.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORECONTAINER
#include "core_container.h"
#endif



int Add_Container(int owner) {
	
	
	circuit c = NewCircuit();
	c.isContainer = 1;
	
	c.dummyin = (int*)calloc(1,sizeof(int));
	c.dummyout = (int*)calloc(1,sizeof(int));
	
	c.updatef = ContainerUpdate;
	
	
	int index = AddToCircuits(c,owner);
	printf("cCore: added container %i\n",index);
	return index;
	
}

void ExternalRelay( circuit *c ) {
    GlobalSignals[c->outputs[0]] = GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[0]];
}
/***********************************************************************
 * This function creates dummy circuits representing composites external
 * channels.
 * ********************************************************************/
int Add_Dummy( int container ) {
    
    //printf("adding dummy\n");
    
    circuit c = NewCircuit();
	
    c.nI = 1;
    c.nO = 1;

    c.updatef = ExternalRelay;
    
    int index = AddToCircuits(c, -1);
    
    //the output is the same as the input
    //circuits[index].outputs = circuits[index].inputs;
    
    
    printf("cCore: added dummy %i \n",index);
    return index;
    
}



int Add_ChannelToContainer(int c, int isInput) {
	
	/*
	int chindex = GlobalChannelCounter;
	GlobalChannelCounter++;
	GlobalSignals = (double*)realloc(GlobalSignals,GlobalChannelCounter*sizeof(double));
	*/
	
	//allocate a new dummy
	int dummyindex = Add_Dummy(-1); //dummy goes in no container, only in global circuits
	
	//allocate the index slot
	if(isInput == 1) {
		
		circuits[c].nI++;
		circuits[c].dummyin = (int*)realloc(circuits[c].dummyin, circuits[c].nI*sizeof(int));
		circuits[c].dummyin[circuits[c].nI-1] = dummyindex;
		
	} else {
		circuits[c].nO++;
		circuits[c].dummyout = (int*)realloc(circuits[c].dummyout, circuits[c].nO*sizeof(int));
		circuits[c].dummyout[circuits[c].nO-1] = dummyindex;
	}
	
	
	return dummyindex;
}

/*********************************************************
 * Container update function
 * ******************************************************/
void ContainerUpdate(circuit* c) {
	
	//printf("updating container: %i\n",c->nsubcircs);
	
	//update time
	GlobalBuffers[circuits[c->dummyout[0]].inputs[0]] += dt;
	GlobalSignals[circuits[c->dummyout[0]].inputs[0]] += dt;
	
	//relay all external inputs
	for (int i = 0; i < c->nI; i++)
	{
		GlobalSignals[circuits[c->dummyin[i]].outputs[0]] = GlobalSignals[circuits[c->dummyin[i]].inputs[0]];
		GlobalBuffers[circuits[c->dummyin[i]].outputs[0]] = GlobalSignals[circuits[c->dummyin[i]].inputs[0]];
	}
	
	
	for (int i = 0; i < c->nsubcircs; i++) {
		//printf("   updating: %i\n",c->subcircuits[i]);
		circuits[c->subcircuits[i]].updatef(&(circuits[c->subcircuits[i]]));
		if(circuits[c->subcircuits[i]].pushed) {
			//update signals
			
			
		}
	}
	
	
	//relay all external outputs
	int idx;
	for (int i = 0; i < c->nO; i++)
	{
		
		idx = circuits[c->dummyout[i]].outputs[0];
		if(i==0) {
			
		
		}
		GlobalBuffers[idx] = GlobalSignals[circuits[c->dummyout[i]].inputs[0]];
		if(c->pushed == 1)
			GlobalSignals[idx] = GlobalBuffers[idx];
		
	}
	
	
	//printf("done\n");
	
	
}
