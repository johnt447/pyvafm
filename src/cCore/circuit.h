#include <stdio.h>

#ifndef CIRCUIT
#define CIRCUIT
#define PI 3.14159265358979323846

// DEFINITION OF CIRCUIT **********************************************
typedef struct circuit circuit;
    
typedef struct circuit {
  
    //number of inputs and outputs
    int nI,nO;

    //indexes of the input, actual and original
    int *inputs, *oinputs; 
    char **inames;

    int *outputs;

    int plen;       //number of double parameters
    double *params; //array of double parameters

    int iplen;      //number of integer parameters
    int *iparams;   //array of integer parameters

    int vplen;      //number of whatever parameters
    void **vpparams;//array of whatever parameters lol
    

    //int update;     //index of the update function
    void (*updatef)(circuit*);  //

    int init;       //index of init function
    
    int pushed;     //0 is false, 1 is true

} circuit;
//*********************************************************************
//int GlobalChannelCounter = 0;
//int GlobalCircuitCounter = 0;

//array containing all signals I and O
//double *GlobalSignals; 


extern double* GlobalSignals;
extern double* GlobalBuffers;
extern int GlobalChannelCounter;

extern circuit* circuits;
extern int GlobalCircuitCounter;

extern void (**ufunctions)(circuit*);
extern char **pynames;

extern double dt;
extern int errorflag;

int AddToCircuits(circuit c);
int GetCircuitIndex(char* type);
circuit NewCircuit(void);


#endif
