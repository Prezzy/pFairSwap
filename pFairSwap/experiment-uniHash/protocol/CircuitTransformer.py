#transform line
#input a line = a gate
#need to ouput a gadget

import os
import binascii
import argparse

from protocol.SecretShare import genSecretShares

    
def transform(lines, P, byteSize):

    wireId = 0
    total = lines.pop(0)
    size = total.split(" ")[1]
    size = int(size)
    index = [None]*(size+1)

    outFileWrite = ""

    inputs = True

    for line in lines:
        print(line)
        parsed = line.split(" ")
        #print(parsed[0])
        if(parsed[0] == "input"):
            wires = []
            inputIndex = int(parsed[1])
            #outFile.write("Begin input expansion\n")
            for i in range(3):
                outFileWrite += "input {}\n".format(wireId)
                wires.append(wireId)
                wireId += 1
            index[inputIndex] = wires

        elif(inputs):
            outFileWrite += "input {}\n".format(wireId)
            oneInput = wireId
            wireId+=1
            inputs = False

        if(parsed[0] == "output"):
            output = int(parsed[1])
            #outFile.write("Begin output expansion\n")
            for i in index[output]:
                outFileWrite += "output {}\n".format(i)

        if(parsed[0] == "add"):
            #outFile.write("Begin add expansion\n")
            print(parsed)
            inWire1 = int(parsed[3].lstrip("<"))
            inWire2 = int(parsed[4].rstrip(">"))
            outWire = int(parsed[7].rstrip(">").lstrip("<"))
            print("parsed: 7 {}".format(parsed[7]))
            print("outWire: {}".format(outWire))
            print(inWire1)
            print(inWire2)

            layer = []
            for i in range(3):
                outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(index[inWire1][i], index[inWire2][i],wireId)
                layer.append(wireId)
                wireId+=1
            index[outWire] = layer
            


        if(parsed[0] == "mul" or parsed[0][0] == "c"):
            layer1 = []
            if(parsed[0] == "mul"):
                #outFile.write("Begin mul expansion\n")
                inWire1 = int(parsed[3].lstrip("<")) 
                inWire2 = int(parsed[4].rstrip(">"))
                outWire = int(parsed[7].rstrip(">").lstrip("<"))

                layer1 = []
                for i in index[inWire1]:
                    seg = []
                    for j in index[inWire2]:
                        outFileWrite += "mul in 2 <{} {}> out 1 <{}>\n".format(i, j, wireId)
                        seg.append(wireId)
                        wireId += 1
                    layer1 += seg
            elif(parsed[0][0:9] == "const-mul"):
                #outFile.write("Begin const-mul expansion\n")
                inWire = int(parsed[3].rstrip(">").lstrip("<"))   #get og input
                outWire = int(parsed[6].rstrip(">").lstrip("<"))   #get og output

                constInfo = parsed[0].split("-")
                secret = int(constInfo[2],16)   #get the const value of mult
                secretShares = genSecretShares(secret, P, byteSize)

                layer1 = []
                for i in secretShares:
                    for j in index[inWire]:
                        outFileWrite += "const-mul-{} in 1 <{}> out 1 <{}>\n".format(i,j,wireId)
                        layer1.append(wireId)
                        wireId+= 1
    
            layer2 = []
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer1[1],layer1[3],wireId)
            layer2.append(wireId)
            wireId += 1

            outFileWrite += "const-mul-{} in 1 <{}> out 1 <{}>\n".format(1, oneInput, wireId)
            layer2.append(wireId)
            wireId += 1

            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer1[2],layer1[6],wireId)
            layer2.append(wireId)
            wireId += 1

            outFileWrite += "const-mul-{} in 1 <{}> out 1 <{}>\n".format(1, oneInput, wireId)
            layer2.append(wireId)
            wireId += 1

            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer1[5],layer1[7],wireId)
            layer2.append(wireId)
            wireId += 1

            outFileWrite += "const-mul-{} in 1 <{}> out 1 <{}>\n".format(1, oneInput, wireId)
            layer2.append(wireId)
            wireId += 1

            layer3 = []
            for i in range(3):
                outFileWrite += "const-mul-neg-{} in 1 <{}> out 1 <{}>\n".format(1,layer2[i*2+1], wireId)
                layer3.append(wireId)
                wireId += 1

            layer4 = []

            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer2[0],layer3[0],wireId)
            layer4.append(wireId)
            wireId += 1
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer2[1],layer2[3],wireId)
            layer4.append(wireId)
            wireId += 1
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer2[2],layer3[1],wireId)
            layer4.append(wireId)
            wireId += 1
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer2[4],layer3[2],wireId)
            layer4.append(wireId)
            wireId += 1

            layer5 = []
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer1[0],layer4[1],wireId)
            layer5.append(wireId)
            wireId += 1
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer4[0],layer2[5],wireId)
            layer5.append(wireId)
            wireId += 1
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer4[2],layer4[3],wireId)
            layer5.append(wireId)
            wireId += 1


            layer6 = []
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer1[4],layer5[1],wireId)
            layer6.append(wireId)
            wireId += 1
            outFileWrite += "add in 2 <{} {}> out 1 <{}>\n".format(layer1[8],layer5[2],wireId)
            layer6.append(wireId)
            wireId += 1

            index[outWire] = layer5[0:1]+layer6
    
    outFileWrite = "total {}\n".format(wireId) + outFileWrite

    return(index, outFileWrite)

