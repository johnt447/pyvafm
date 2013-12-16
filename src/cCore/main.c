#include <stdio.h>

//#include "circuit.c"

//#include "main.h"


/**********************************************************
The python system will just call
functions in the library that will internally setup the vafm
and run it at uberspeed.
***********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#include "core_maths.h"

// *** GLOBAL DEFINITIONS **********************************
double dt;
int GlobalChannelCounter = 0; //counter for channels
int GlobalCircuitCounter = 0; //counter for citcuits


int GlobalNFunctions;
void **ifunctions; //list of pointers to function: circuit initialisers
void (**ufunctions)(circuit*); //list of pointers to function: circuit updaters
char **pynames;    //list of python names for the circuits

//array containing all signals I and O
double *GlobalSignals, *GlobalBuffers; 


circuit *circuits;

int newcircuits = 1;

int errorflag = 0;

// *********************************************************
int AllocateCircuits(void);
int INIT(void);


int INIT(void) {
  
  dt = 0.01;
  
  AllocateCircuits();
  



  printf("VAFMCORE: initialised!\n");


  /*

  //initialize some feeds (includes I and O)
  //... this can be automatized...
  GlobalSignals = (double*) calloc (20,dsize);
  
  //python could call these function to create 
  //circuits in the C library
  AddCircuit("opMUL",2,1);
  AddCircuit("opADD",2,1);

  circuits[1].inputs[0] = 2;
  GlobalSignals[circuits[1].inputs[1]] = 0.09;

  printf("outputs: %lf %lf\n",
	 GlobalSignals[circuits[0].outputs[0]],
	 GlobalSignals[circuits[1].outputs[0]]);
  
  Update();
  printf("outputs: %lf %lf\n",
	 GlobalSignals[circuits[0].outputs[0]],
	 GlobalSignals[circuits[1].outputs[0]]);
  
  GlobalSignals[0] = 1.3;
  GlobalSignals[1] = 2;

  Update();
  printf("outputs: %lf %lf\n",
	 GlobalSignals[circuits[0].outputs[0]],
	 GlobalSignals[circuits[1].outputs[0]]);

  */

  return 0;
}



int AllocateCircuits() {


  GlobalNFunctions = 100; //correct this!
  ifunctions = (void**)malloc(GlobalNFunctions*sizeof(void*));
  ufunctions = (void**)malloc(GlobalNFunctions*sizeof(void*));
  pynames = (char**)malloc(GlobalNFunctions*sizeof(char*));
  circuits = (circuit*)calloc(1,sizeof(circuit));
  
  GlobalSignals = (double*)calloc(1,sizeof(double)); //signal 0 is the time
  GlobalBuffers = (double*)calloc(1,sizeof(double)); //signal 0 is the time
  GlobalChannelCounter = 1;

  int i=0;
  INIT_MATHS(&i);
  INIT_LOGIC(&i);
  INIT_SIGNALS(&i);
  INIT_FILTERS(&i);
  INIT_OUTPUT(&i);

  

  return 0;
}

//deallocate resources
int QUIT() {
  
  free(pynames);
  free(ufunctions); free(ifunctions);
  

}


/***********************************************************************
 * Internal function. Allocates the channel indexers and the signals for
 * circuit c.
***********************************************************************/
int AddChannels( circuit *c ) {
  
  if(c->nI > 0) {
    c->inputs = (int*)calloc(c->nI,sizeof(int));
    c->oinputs = (int*)calloc(c->nI,sizeof(int));
    for(int i=0;i<c->nI;i++) {
      c->inputs[i] = GlobalChannelCounter;
      c->oinputs[i] = GlobalChannelCounter;
      GlobalChannelCounter++;
    }
  }

  if(c->nO > 0) {
    c->outputs= (int*)calloc(c->nO,sizeof(int));
    for(int i=0;i<c->nO;i++) {
      c->outputs[i] = GlobalChannelCounter;
      GlobalChannelCounter++;
    }
  }
  GlobalSignals = (double*)realloc(GlobalSignals,sizeof(double)*GlobalChannelCounter);
  GlobalBuffers = (double*)realloc(GlobalBuffers,sizeof(double)*GlobalChannelCounter);

  return 0;
}

/*int MakeChannels( circuit *c, int ni, int no ) {
  
  c->nI = ni;
  c->nO = no;

  c->inputs = (int*)calloc(ni,sizeof(int));
  c->oinputs = (int*)calloc(ni,sizeof(int));
  for(int i=0;i<ni;i++) {
    c->inputs[i] = GlobalChannelCounter;
    c->oinputs[i] = GlobalChannelCounter;
    GlobalChannelCounter++;
  }

  c->outputs= (int*)calloc(no,sizeof(int));
  for(int i=0;i<no;i++) {
    c->outputs[i] = GlobalChannelCounter;
    GlobalChannelCounter++;
  }

  
  return 0;
}
*/

/***********************************************************************
 * Makes a new empty circuit.
***********************************************************************/
circuit NewCircuit() {
    
    circuit c;
    c.iplen = 0;
    c.plen = 0;
    c.vplen = 0;
    //c.updatef = DummyCircuit;
    c.nI = 0;
    c.nO = 0;
    c.pushed = 0; //false by default
    
    return c;
}
/***********************************************************************
 * Sets the behaviour of the circuit with index cindex.
 * 0 is not pushed, 1 is pushed.
 * Python callable.
***********************************************************************/
int SetPushed(int cindex, int pushed) {
    
    circuits[cindex].pushed = pushed;
    
    return 0;
}

/***********************************************************************
 * This function makes a new slot in the circuits list and stores the
 * new one given as argument. Returns the index of the new circuit.
***********************************************************************/
int AddToCircuits(circuit c) {
    
    AddChannels(&c); //allocates the signals
    
    GlobalCircuitCounter++;
    circuits = (circuit*)realloc(circuits, GlobalCircuitCounter*sizeof(circuit));
    circuits[GlobalCircuitCounter-1] = c;
    
    //printf("param0: %lf \n",c.params[0]);
    
    return GlobalCircuitCounter-1;
}


void DummyCircuit( circuit *c ) {
    GlobalSignals[c->outputs[0]] = GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[0]];
}
/***********************************************************************
 * This function creates dummy circuits representing composites external
 * channels.
 * ********************************************************************/
int Add_Dummy( ) {
    
    circuit c = NewCircuit();

    c.nI = 1;
    c.nO = 1;

    c.updatef = DummyCircuit;
    
    int index = AddToCircuits(c);
    
    //the output is the same as the input
    //circuits[index].outputs = circuits[index].inputs;
    
    
    //printf("Added maths [%s].\n",type);
    return index;
    
}


/***********************************************************************
 * Get the index of a circuit named "type" in the template list.
***********************************************************************/
int GetCircuitIndex(char* type) {
    
    //find the function name in the list
    for(int i=0; i<GlobalNFunctions; i++) {
        if(strcmp(pynames[i],type) == 0) {
            return i;
        }
    } 
    printf("cERROR: circuit of type [%s] was not found!",type);
    return -1; //not found!
}

//create a circuit
/*int AddCircuit(char* type, int ni, int no) {

  //check if the library is initialised! TODO
  
  
  circuit c;
  MakeChannels(&c,ni,no); //make the channels
  GlobalSignals = (double*)realloc(GlobalSignals,sizeof(double)*GlobalChannelCounter);


  //allocate a new slot for circuit
  GlobalCircuitCounter++;
  circuits = (circuit*)realloc(circuits, GlobalCircuitCounter*sizeof(circuit));
  

  //find the function name in the list
  for(int i=0; i<GlobalNFunctions; i++) {
    if(strcmp(pynames[i],type) == 0) {
      
      c.update = i; //set the update function index

      break;
    }
  }
  
  //store the new circuit in the array
  circuits[GlobalCircuitCounter-1] = c;

  //return &(circuits[GlobalCircuitCounter-1]);
  printf("Added circuit: %s\n",type);

  newcircuits = 1;

  //return the index of the circuit
  return GlobalCircuitCounter-1;
}
*/

//connect function
int Connect(int c1, int out, int c2, int in) {
  
  circuits[c2].inputs[in] = circuits[c1].outputs[out];
  

  return 0;
}


int SetInput(int c, int inidx, double value){

  GlobalSignals[circuits[c].inputs[inidx]] = value;
  GlobalBuffers[circuits[c].inputs[inidx]] = value;
  
  return 0;
}


int Update(int steps) {
 
    for(int t=0; t<steps; t++) {
    //printf("step %d\n",t);

        for(int i=0; i<GlobalCircuitCounter; i++){
            //printf("circuit[%d] function[%d]\n",i,circuits[i].update);
            //ufunctions[circuits[i].update]( &circuits[i] );
            circuits[i].updatef( &circuits[i] ); //this way is faster
            if(circuits[i].pushed == 1) {
                for (int k = 0; k < circuits[i].nO; k++) {
                    GlobalSignals[circuits[i].outputs[k]] = GlobalBuffers[circuits[i].outputs[k]];
                }
                
            }
        }
        
        //now push all
        for (int i = 0; i < GlobalChannelCounter; i++)
        {
            GlobalSignals[i] = GlobalBuffers[i];
        }
        /*for(int i=0; i<GlobalCircuitCounter; i++){
            
            if(circuits[i].pushed == 1) continue;
            
            for (int k = 0; k < circuits[i].nO; k++) {
                    GlobalSignals[circuits[i].outputs[k]] = GlobalBuffers[circuits[i].outputs[k]];
                }
        }*/ //this is slower than updating all buffers

    GlobalBuffers[0] += dt;
    GlobalSignals[0] = GlobalBuffers[0];

    }
    printf("steps %d\n",steps);

    return 0;
}


int Status(void) {

  
  for(int i=0; i<GlobalCircuitCounter; i++) {
    
    printf("circuit [%d]:\t%ld\n",i,circuits[i].updatef);
    
  }
  
}


int DebugCircuit(int c){


  printf("circuit [%i]: %i in  %i out \n",c,circuits[c].nI,circuits[c].nO);
  for(int i=0; i<circuits[c].nI; i++){
    printf("  in[%i]: signal[%i] value[%lf] buffered[%lf]\n",i,circuits[c].inputs[i],GlobalSignals[circuits[c].inputs[i]],GlobalBuffers[circuits[c].inputs[i]]);
  }

  for(int i=0; i<circuits[c].nO; i++){
    printf(" out[%i]: signal[%i] value[%lf] buffered[%lf]\n",i,circuits[c].outputs[i],GlobalSignals[circuits[c].outputs[i]],GlobalBuffers[circuits[c].outputs[i]]);
  }

  for(int i=0; i< circuits[c].iplen; i++){
    printf("  ip[%i]: value[%i]\n",i,circuits[c].iparams[i]);
  }

  return 0;
}
