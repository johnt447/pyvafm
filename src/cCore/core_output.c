/**********************************************************
Output circuits definitions.
 *********************************************************/
#include <stdio.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREOUTPUT
#include "core_output.h"
#endif



int Add_output(int owner, char* filename, int dump) {

    circuit c = NewCircuit();

    c.nI = 1;
    c.nO = 0;

    c.iplen = 3;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    c.iparams[0] = dump;
    c.iparams[1] = 0; //step counter
    c.iparams[2] = 0; //number of channels to print

    c.vplen = 1;
    c.vpparams = (void**)malloc(sizeof(FILE*));//one element
    c.vpparams[0] = (void*)fopen(filename, "w");

    c.updatef = output;

    //*** ALLOCATE IN LIST *********************
    int index = AddToCircuits(c, owner);

    printf("Added output %i.\n",index);
    return index;
    
}

int output_register(int outer, int cindex, int chindex, int isInput) {

    circuits[outer].iparams[2]++;
    circuits[outer].iplen+=3;
    circuits[outer].iparams = (int*)realloc(circuits[outer].iparams,
        circuits[outer].iplen*sizeof(int));
    //printf("reallocating to size: %d\n",(2+circuits[outer].iparams[1]));
    
    circuit *owner = &(circuits[cindex]);
    if(owner->isContainer == 1) {
        
        int dummy = (isInput==1)? owner->dummyin[chindex] : owner->dummyout[chindex];
        circuits[outer].iparams[circuits[outer].iplen-3] = dummy;
        circuits[outer].iparams[circuits[outer].iplen-2] = 0;
        circuits[outer].iparams[circuits[outer].iplen-1] = isInput;
        
    }
    else {
        
        //circuit ID
        circuits[outer].iparams[circuits[outer].iplen-3] = cindex;
        circuits[outer].iparams[circuits[outer].iplen-2] = chindex;
        circuits[outer].iparams[circuits[outer].iplen-1] = isInput;
    }
    
    return 0;
}

int output_register_feedasd(int outer, int feedid) {

    circuits[outer].iparams[2]++;
    circuits[outer].iplen++;
    circuits[outer].iparams = (int*)realloc(circuits[outer].iparams,
            circuits[outer].iplen*sizeof(int));

    circuits[outer].iparams[circuits[outer].iplen-1] = feedid;
    
    return 0;
}

void output_dump( int index ) {
    
    //circuits[index].updatef(&(circuits[index]));
    output_printout( &(circuits[index]) );
}

/*void output_printout( circuit *c ) {
    
    for(int i=3; i < c->iplen; i++){
        
        //printf("%lf ",GlobalSignals[c->iparams[i]]);
        fprintf((c->vpparams[0]), "%15.8lf ", GlobalSignals[c->iparams[i]]);
        
    }
    //printf("\n");
    fprintf((c->vpparams[0]), "\n");
}*/
void output_printout( circuit *c ) {
    
    for(int i=3; i < c->iplen; i+=3){
        
        //printf("%lf ",GlobalSignals[c->iparams[i]]);
        int feedidx;
        if(c->iparams[i+2] == 1) 
            feedidx = circuits[c->iparams[i]].inputs[c->iparams[i+1]];
        else
            feedidx = circuits[c->iparams[i]].outputs[c->iparams[i+1]];
        
        fprintf((c->vpparams[0]), "%15.8lf ", GlobalSignals[feedidx]);
        
    }
    //printf("\n");
    fprintf((c->vpparams[0]), "\n");
}

int output_close(int outer) {
  
  fclose(circuits[outer].vpparams[0]);
  
  return 0;
}

void output( circuit *c ) {

    if(c->iparams[0] <= 0) {
        //printf("asd!\n");
        if(GlobalSignals[c->inputs[0]] > 0) {
            output_printout(c); //do the print out
        }
        
        return;
    }
    
    c->iparams[1]++;
    
    if(c->iparams[1] >= c->iparams[0]) {
        
        output_printout(c); //do the print out
        c->iparams[1] = 0;
    
    }

}


