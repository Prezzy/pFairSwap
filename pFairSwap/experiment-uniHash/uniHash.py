import argparse
import os
import math
def uniHash(key, msg, numChunks, keyLen):
    print("uniHASH: {}".format(key[0].decode("utf-8")))

    i = 0
    temp = 0
    while(i < numChunks):
            j = 0
            temp = pow(temp * int(key[0].hex()),1,(2**1279)-1)
            for j in range(1,keyLen):

                #print(type(msg[i]))
                #print(msg[i])
                #print(type(key[j]))
                #print(key[j])
                temp += pow(int(msg[i], 16) * int(key[j].hex()),1,(2**1279)-1)
                i += 1

    return temp

def writeInputFile(numChunks, chunkSize, keys, name, inputFile):
    inFile = open(inputFile, "rb")
    circuitInputs = open("inputs-{}".format(name), "w")

    numKeys = len(keys)

    index = 0

    for i in keys:
        circuitInputs.write("{} 0x{}\n".format(index, i.decode("utf-8")))
        index += 1

    bytez = inFile.read(chunkSize)
    while len(bytez) > 0:
        circuitInputs.write("{} 0x{}\n".format(index, bytez.hex()))
        index += 1
        bytez = inFile.read(chunkSize)

    temp_index = index
    for i in range(temp_index,numChunks+numKeys):
        circuitInputs.write("{} 0x0\n".format(index))
        index += 1

    circuitInputs.write("{} 0x1".format(index))

    circuitInputs.close()
    inFile.close()
        




def writeCFiles(numChunks, keyLen, name):
    print("creating circuit for {}".format(name))
    cFile = open("../uniHash-{}.c".format(name), "w")
    headerFile = open("../uniHash-{}-ifc.h".format(name), "w")

    cSource = ''

    cSource += '#include "uniHash-{}-ifc.h"\n\n'.format(name)
    cSource += 'void outsource(struct Input *input, struct Output *output)\n'
    cSource += '{\n'
    cSource += '   unsigned int i,j,temp;\n\n'
    cSource += '   i = 0;\n'
    cSource += '   temp = 0;\n'
    cSource += '   while(i < NUMCHUNKS)\n'
    cSource += '   {\n'
    cSource += '       j = 0;\n'
    cSource += '       temp = temp * input->key[0];\n'
    cSource += '      for(j=1; j < KEYLEN; j+=1)\n'
    cSource += '      {\n'
    cSource += '          temp += input->msg[i] * input->key[j];\n'
    cSource += '          i += 1;\n'
    cSource += '      }\n'
    cSource += '  }\n'
    cSource += '  output->hash[0] = temp;\n'
    cSource += '}'

    headerLines = ''

    headerLines += '#define NUMCHUNKS {}\n'.format(numChunks)
    headerLines += '#define KEYLEN {}\n\n'.format(keyLen)

    headerLines += 'struct Input {\n'
    headerLines += '   unsigned int key[KEYLEN];\n'
    headerLines += '   unsigned int msg[NUMCHUNKS];\n'
    headerLines += '};\n\n'

    headerLines += 'struct Output {\n'
    headerLines += '   unsigned int hash[1];\n'
    headerLines += '};\n\n'

    headerLines += 'void outsource(struct Input *input, struct Output *output);'

    cFile.write(cSource)
    headerFile.write(headerLines)


def createCircuit(feild, fileSize, inputFile):

    chunkSize = feild//8
    numChunks = math.ceil(fileSize/chunkSize)
    targetLen = math.ceil(numChunks / 20)  #20 is key size
    numChunks += (20*targetLen) - numChunks

    keyFile = open("key-{}".format(feild), "rb")
    keys = keyFile.read().splitlines()

    writeInputFile(numChunks, chunkSize, keys, feild, inputFile)
    writeCFiles(numChunks, 21, feild)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputFile", help="Name of the file to process as input", required=True)
    parser.add_argument("--lambda", help="size of each input chunk in bits")
    parser.add_argument("--numChunks", help="The number of chunks that you will use")
    parser.add_argument("--keyLen", help="The number of elements in the key")

    args = parser.parse_args()

    st = os.stat(args.inputFile)
    fileSize = st.st_size

    #print(fileSize)
    feilds = [1279, 607, 521, 127, 107, 89]

    #chunkSize = 1279//8
    #numChunks = math.ceil(fileSize/chunkSize)
    #goal = math.ceil(numChunks / 20)
    #numChunks += (20*goal)-numChunks
    #print(numChunks)
    #keyFile = open("key-1279", "rb")
    #keys = keyFile.read().splitlines()
    #writeInputFile(numChunks, chunkSize, keys, 1279, args.inputFile)
    #writeCFiles(numChunks, 21, 1279)

    for feild in feilds:
        createCircuit(feild, fileSize, args.inputFile)


    #inFile = open(args.inputFile, "rb")
    
    #msg = []
    #bytez = inFile.read(chunkSize)
    #while len(bytez) > 0:
        #msg.append(bytez.hex())
        #bytez = inFile.read(chunkSize)

    #paddingLength = numChunks - len(msg)
    #if paddingLength > 0:
         #msg += ['0'] * paddingLength

    

    #final = uniHash(keys, msg, numChunks, 21)
    #print("final {}".format(hex(final)))


    
main()

