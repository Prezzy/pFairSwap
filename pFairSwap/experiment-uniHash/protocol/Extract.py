import re
import argparse
from protocol.merkleTree import makeMerkleTree, mProof, mVrfy

#function to turn lines of the circuit file into a data structure that can be indexed

def parsePhi(phi):
    phiStructure = []
    for gate in phi:
        gateParts = gate.split(" ")
        if (gateParts[0] == "total"):
            numWires = int(gateParts[1])
            phiStructure = [0] * numWires
        elif (gateParts[0] == "input"):
            wireId = int(gateParts[1])
            phiStructure[wireId] = gateParts[0]
        elif (gateParts[0] == "output"):
            continue
        else:
            numIn = gateParts[2]
            op = gateParts[0]
            if(int(numIn) == 2):
                in1 = gateParts[3]
                in2 = gateParts[4]
                data = "{}, {} {}".format(op, in1, in2)
                wireId = gateParts[7].rstrip('\n').rstrip('>').lstrip('<')
            else:
                data = "{}, {}".format(op, gateParts[3])
                wireId = gateParts[6].rstrip('\n').rstrip('>').lstrip('<')
            #print(op)
            #print(I)
            phiStructure[int(wireId)] = data
    return phiStructure

#Everything below has recieved very little attention

def processPhi(phi):
    print("Making Merkle Tree of phi")
    mPhiTree = makeMerkleTree(phi)
    mPhiTreeRoot = mPhiTree[0]
    mPhiTree.reverse()
    return(mPhiTreeRoot, mPhiTree)

def processZ(sellerLines):
    print("Making Merkle Tree for z")
    mZTree = makeMerkleTree(sellerLines)
    print("Getting Merkle root of Merkle Tree for z")
    mZTreeRoot = mZTree[0]
    mZTree.reverse()
    return (mZTreeRoot, mZTree)



def recievKey(keyFile):
    print("Roots match, Key is revealed...\n\n")
    key = keyFile.read()
    key = bytes.fromhex(key)

    return key



def checkComp(sellerLines, buyerLines, key, mPhiTreeRoot, mPhiTree, mZTreeRoot, mZTree, phiFile):
    phiLines = phiFile.readlines()
    phi = parsePhi(phiLines)
    for i in range(len(sellerLines)):
        sellData = sellerLines[i].split(" ")
        sellIndex = sellData[0]
        sellCipher = sellData[1].rstrip()

        buyData = buyerLines[i].split(" ")
        buyIndex = buyData[0]
        buyPlain = buyData[1].rstrip()

        sellPlain = dec(int(sellIndex), key, int(sellCipher, 16)).hex()

        if(int(sellIndex) == 23):
            print("Buyer find problem and creates PoM")
            POM = [0] * 4
            print("Generate gate proof\n")
            gateProof = mProof(int(sellIndex), mPhiTree)
            print(phi[int(sellIndex)])
            print("Validity of gate proof {}\n\n".format(mVrfy(int(sellIndex),phi[int(sellIndex)], gateProof, mPhiTreeRoot)))
            POM[0] = gateProof
            gateDes = phi[int(sellIndex)]
            gateDes = gateDes.split(" ",1)
            if (gateDes[0] == "total"):
                #do something
                pass
            elif (gateDes[0] == "input"):
                #do something
                pass
            elif (gateDes[0] == "output"):
                pass
            else:
                gateInfo = re.split(' |<|>',gateDes[1])
                numIn = gateInfo[1]
                if(int(numIn) == 2):
                    outputID = gateInfo[9]
                    I = gateInfo[3:5]
                else:
                    outputID =gateInfo[8]
                    I = [gateInfo[3]]
            print("Generate out_i proof\n")
            print(sellerLines[int(outputID)])
            outProof = mProof(int(outputID),mZTree)
            print("validity of out_i proof {}\n\n".format(mVrfy(int(outputID),sellerLines[int(outputID)],outProof,mZTreeRoot)))
            POM[1] = outProof
            print(int(I[0]))
            for i in range(len(I)):
                print("Generate input {} proof\n".format(i))
                print(sellerLines[int(I[i])])
                inProof = mProof(int(I[i]), mZTree)
                print("validity of input {} proof {}\n\n".format(i,mVrfy(int(I[i]),sellerLines[int(I[i])],inProof,mZTreeRoot)))
                POM[i+2] = inProof

    return POM


