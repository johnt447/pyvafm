#include <stdio.h>

#ifndef CIRCUIT
#define CIRCUIT

// DEFINITION OF CIRCUIT **********************************************
typedef struct circuit {
  
    int nI,nO;

    int *inputs, *oinputs; //indexes of the input, actual and original
    char **inames;

    int *outputs;

    int plen;
    double *params; //double float parameters

    int iplen;
    int *iparams; //integer parameters

    int vplen;
    void **vpparams; //list of pointers to void
    //FILE *fp;

    int update; //index of the update function
    void *updatef;

    int init;   //index of init function

} circuit;
//*********************************************************************
//int GlobalChannelCounter = 0;
//int GlobalCircuitCounter = 0;

//array containing all signals I and O
//double *GlobalSignals; 


extern double* GlobalSignals;
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
