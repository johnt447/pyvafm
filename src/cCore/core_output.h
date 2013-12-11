#ifndef COREOUTPUT
#define COREOUTPUT


int Add_output( char* filename, int dump );
void output( circuit *c );
int output_register (int, int, int);
int output_close(int outer);


#endif
