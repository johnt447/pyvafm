/**********************************************************
Interpolation circuits definitions.
*********************************************************/
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREINTER
#include "core_interpolation.h"
#endif

int Add_i3Dlin( int owner, float* pointer, int size, int components, 
	double xstep, double ystep, double zstep, double xmin, double ymin, double zmin, 
	int xsize, int ysize, int zsize) {
	
    circuit c = NewCircuit();
    c.nI = 3;
    c.nO = components;

    c.plen = components*size+11;
    c.params = (double*)calloc(c.plen,sizeof(double));
    int i;
    for (i=0;i<size*components; i++)
    {
        c.params[i] = *(pointer+i);
    }

    c.params[size*components+1] = xstep;
    c.params[size*components+2] = ystep;
    c.params[size*components+3] = zstep;
    c.params[size*components+4] = xmin;
    c.params[size*components+5] = ymin;
    c.params[size*components+6] = zmin;


    c.iplen = 6;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));

    c.iparams[0] = size;
    c.iparams[1] = components;
    c.iparams[2] = xsize;
    c.iparams[3] = ysize;
    c.iparams[4] = zsize;
    c.iparams[5] = 0; //counter

    c.updatef = i3Dlin; //this is the default scanner update function
    int index = AddToCircuits(c,owner);
    printf("cCore: i3Dlin initialised\n");
    return index;

}



void i3Dlin( circuit *c )
 {
    if (c->iparams[5] != 0){

        int CompCounter;
        for (CompCounter=0;CompCounter<c->iparams[1];CompCounter++){

    double x = GlobalSignals[c->inputs[0]];
    double y = GlobalSignals[c->inputs[1]];
    double z = GlobalSignals[c->inputs[2]];



    int size = c->iparams[0];
    int components = c->iparams[1];

    double gridstepx = c->params[size*components+1];
    double gridstepy = c->params[size*components+2];
    double gridstepz = c->params[size*components+3];
    double xmin = c->params[size*components+4];
    double ymin = c->params[size*components+5];
    double zmin = c->params[size*components+6];
    int xsize = c->iparams[2];
    int ysize = c->iparams[3];
    int zsize = c->iparams[4];


    // find the voxel the point is in
    double voxelstepx = x / gridstepx;
    double xo = floor(voxelstepx) * gridstepx;

    double voxelstepy = y / gridstepy;
    double yo = floor(voxelstepy) * gridstepy;

    double voxelstepz = z / gridstepz;
    double zo = floor(voxelstepz) * gridstepz;

    double xd = (x-xo) / ( (xo + gridstepx) - xo );
    double yd = (y-yo) / ( (yo + gridstepy) - yo );
    double zd = (z-zo) / ( (zo + gridstepz) - zo );


    //so the counter starts at 0 instead of whatveer the min value of each array is allowing for a correct starting poistion for the counting
    int i = xo-xmin;
    int j = yo-ymin;
    int k = zo-zmin;

    int tracker = (xsize * (i) + ysize * (j) + k )+CompCounter*c->iparams[0];

    double Fooo = c->params[tracker];

    
    //2
    //x+1 , y ,z
    tracker = (xsize * (i+gridstepx) + ysize * (j) + k )+CompCounter*c->iparams[0];
    double Fioo = c->params[tracker];
    
    //3
    //x+1, y+1, z
    tracker = (xsize * (i+gridstepx) + ysize * (j+gridstepy) + k )+CompCounter*c->iparams[0];
    double Fiio = c->params[tracker];
   
    //4
    //x+1,y+1,z+1
    tracker = (xsize * (i+gridstepx) + ysize * (j+gridstepy) + k+gridstepz )+CompCounter*c->iparams[0];
    double Fiii = c->params[tracker];
    

    //5
    //x,y+1,z
    tracker = (xsize * (i) + ysize * (j+gridstepy) + k )+CompCounter*c->iparams[0];
    double Foio = c->params[tracker];
    
    //6
    //x,y,z+1
    tracker = (xsize * (i) + ysize * (j) + k+gridstepz )+CompCounter*c->iparams[0];
    double Fooi = c->params[tracker];



    //7
    //x,y+1,z+1
    tracker = (xsize * (i) + ysize * (j+gridstepy) + k+gridstepz )+CompCounter*c->iparams[0];
    double Foii = c->params[tracker];
    

    //8
    //x+1,y,z+1
    tracker = (xsize * (i+gridstepx) + ysize * (j) + k+gridstepz )+CompCounter*c->iparams[0];
    double Fioi = c->params[tracker];

    
    /*
printf("Fooo %f %f %f %e \n", xo,yo,zo , Fooo);
printf("Fioo %f %f %f %e \n", xo+1,yo,zo , Fioo);
printf("Fiio %f %f %f %e \n", xo+1,yo+1,zo , Fiio);
printf("Fiii %f %f %f %e \n", xo+1,yo+1,zo+1 , Fiii);
printf("Foio %f %f %f %e \n", xo,yo+1,zo , Foio);
printf("Fooi %f %f %f %e \n", xo,yo,zo+1 , Fooi);
printf("Foii %f %f %f %e \n", xo,yo+1,zo+1 , Foii);
printf("Fioi %f %f %f %e \n", xo+1,yo,zo+1 , Fioi);
*/


    double coo = Fooo * (1-xd) + Fioo*xd;
    double cio = Foio * (1-xd) + Fiio*xd;
    double coi = Fooi * (1-xd) + Fioi*xd;
    double cii = Foii * (1-xd) + Fiii*xd;

    double co = coo*(1-yd) + cio*yd;
    double ci = coi*(1-yd) + cii*yd;

    double answer = co * (1-zd) + ci*zd;
    GlobalBuffers[c->outputs[CompCounter]] = answer;
        }
    }



    c->iparams[5]++;
}
