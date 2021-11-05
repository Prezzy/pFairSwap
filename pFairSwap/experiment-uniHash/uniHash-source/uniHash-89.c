#include "uniHash-89-ifc.h"

void outsource(struct Input *input, struct Output *output)
{
   unsigned int i,j,temp;

   i = 0;
   temp = 0;
   while(i < NUMCHUNKS)
   {
       j = 0;
       temp = temp * input->key[0];
      for(j=1; j < KEYLEN; j+=1)
      {
          temp += input->msg[i] * input->key[j];
          i += 1;
      }
  }
  output->hash[0] = temp;
}