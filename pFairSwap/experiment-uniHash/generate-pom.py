from protocol.Extract import parsePhi, processPhi, processZ, recievKey
from protocol.encryption import key_gen, dec
from protocol.Encode import encodeWire
from protocol.MrkTree import MerkleTree, mVrfy
import copy

def createPOM(sellerLines, phiLines, phiMroot, phiMtree, zMroot, zMtree, idx):
    phi = phiLines

    for line in sellerLines:
        sellData = line.split(" ")
        sellIndex = sellData[0]
        sellCipher = sellData[1].rstrip()

        #sellPlain = dec(int(sellIndex), key, int(sellCipher, 16)).hex()


        if(int(sellIndex) == idx):
            print("generating POM...")
            print("generate gate description proof...")
            print(int(sellIndex))
            gateProof = mProof(0, phiMtree)
            print(phiMtree)
            print("------------")
            print(gateProof)

            print("gate proof verify {}".format(mVrfy(int(sellIndex), sellerLines[idx], gateProof, phiMroot)))



            gateDes = phi[int(sellIndex)]
            gateDes = gateDes.split(" ")

            in1Idx = gateDes[1][1:] 
            in2Idx = gateDes[2][:-1]

            print(int(in1Idx))
            print(int(in2Idx))
            print(sellerLines[int(in1Idx)])
            print(sellerLines[int(in2Idx)])
            in1Proof = mProof(int(in1Idx), zMtree)

            in2Proof = mProof(int(in2Idx), zMtree)

            outProof = mProof(idx, zMtree)
            print(sellerLines[idx])



            
def getHex(string):
    hexString = string.split(" ")[1]
    return hexString.replace("0x", "", 1)



def prettyProof(proof):
    proofString = "["
    for i in proof[:-1]:
        proofString += "\"{}\",".format(i.hex())

    proofString += "\"{}\"]".format(proof[-1].hex())

    return proofString



def main():
    outIdx = 6781
    sellerFile = open("wires/wires-89", "r")
    sellerLines = sellerFile.readlines()
    circuitFile = open("circuits/uniHash-89.arith", "r")
    circuitLines = circuitFile.readlines()

    phi = parsePhi(circuitLines)
    print("out plain -{}".format(sellerLines[outIdx]))
    #get indexes of input gates to gate idx
    gateDes = phi[outIdx]
    print(gateDes)

    if(gateDes == "input"):
        print("Complaining about input gate, nothing to do")
        return

    gateDes = gateDes.split(" ")
    in1Idx = int(gateDes[1][1:]) 
    in2Idx = int(gateDes[2][:-1])

    inVal1 = int(sellerLines[in1Idx].split(" ")[1],0)
    inVal2 = int(sellerLines[in2Idx].split(" ")[1],0)

    outVal = int(sellerLines[outIdx].split(" ")[1],0)

    print("result - {}".format(pow(inVal1 * inVal2,1,(2**89)-1)))
    print("inval1 - {}".format(inVal1))
    print("inval2 - {}".format(inVal2))
    print("out - {}".format(outVal))

    print("gateDes - {}".format(gateDes))
    print("in1 - {}".format(sellerLines[in1Idx]))
    print("in2 - {}".format(sellerLines[in2Idx]))
    print("out - {}".format(sellerLines[outIdx]))

    wires = copy.deepcopy(sellerLines)

    keyFile = open("key", "rb")

    key = keyFile.read(32)

    #key = key_gen(16)



    encodedWires = encodeWire(wires, key).split('\n')

    encodedWires = encodedWires[:-1]

    for i in range(len(encodedWires)):
        encodedWires[i] = bytes.fromhex(encodedWires[i])


    dec(outIdx, key, encodedWires[outIdx])


    phiMerkleTree = MerkleTree(phi)
    zMerkleTree = MerkleTree(encodedWires)

    PoMFile = open("PoM", "w")

    gateEle = phi[outIdx]
    outEle = encodedWires[outIdx]
    print(outEle)
    in1Ele = encodedWires[in1Idx]
    in2Ele = encodedWires[in2Idx]

    gateProof = phiMerkleTree.mProof(outIdx)
    outProof = zMerkleTree.mProof(outIdx)
    in1Proof = zMerkleTree.mProof(in1Idx)
    in2Proof = zMerkleTree.mProof(in2Idx)


    print("outProof len - {}".format(len(outProof)))
    print("inProof len - {}".format(len(in1Proof)))
    print("inProof len- {}".format(len(in2Proof)))
    print("gateProof - {}".format(len(gateProof)))

    PoMFile.write("gate index {}\n".format(outIdx))
    PoMFile.write("gate des {}\n".format(gateEle))
    PoMFile.write("gate proof {}\n\n".format(prettyProof(gateProof)))

    PoMFile.write("out index {}\n".format(outIdx))
    PoMFile.write("out element 0x{}\n".format(outEle.hex()))
    PoMFile.write("out proof index {}\n\n".format(prettyProof(outProof)))

    PoMFile.write("in1 index {}\n".format(in1Idx))
    PoMFile.write("in1 ele 0x{}\n".format(in1Ele.hex()))
    PoMFile.write("in1 proof {}\n\n".format(prettyProof(in1Proof)))

    PoMFile.write("in2 index {}\n".format(in2Idx))
    PoMFile.write("in2 ele 0x{}\n".format(in2Ele.hex()))
    PoMFile.write("in2 proof {}\n\n".format(prettyProof(in2Proof)))

    PoMFile.write("Z Root: {}\n".format(zMerkleTree.root.hex()))
    PoMFile.write("phi Root: {}\n".format(phiMerkleTree.root.hex()))

    PoMFile.write("key: 0x{}".format(key.hex()))

    #print(len(proof))
    #proofString = "["
    #for i in proof[:-1]:
    #    proofString += "\"{}\",".format(i.hex())

    #proofString += "\"{}\"]".format(proof[-1].hex())

    print(mVrfy(outIdx, phi[outIdx], gateProof, phiMerkleTree.root))
    print(mVrfy(outIdx,encodedWires[outIdx], outProof, zMerkleTree.root))
    print(mVrfy(in1Idx,encodedWires[in1Idx], in1Proof, zMerkleTree.root))
    print(mVrfy(in2Idx,encodedWires[in2Idx], in2Proof, zMerkleTree.root))




main()
