#ifndef CORESIGNALPROCESSING
#define CORESIGNALPROCESSING

int Add_Gain(int owner, double gain) ;
void Gain( circuit *c );

int Add_minmax(int owner, double checktime);
void minmax( circuit *c );

void derivative(circuit *c);
void integral(circuit *c);
void delay(circuit *c);
void peaker(circuit *c);
void phasor(circuit *c);


#endif
