#define NUMCHUNKS 5120
#define KEYLEN 21

struct Input {
   unsigned int key[KEYLEN];
   unsigned int msg[NUMCHUNKS];
};

struct Output {
   unsigned int hash[1];
};

void outsource(struct Input *input, struct Output *output);