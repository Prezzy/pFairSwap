import time
from protocol.Encode import encodeWire
from protocol.encryption import key_gen

loopCount = 5

def main():

    key = key_gen(32)


    fields = [127, 107, 89]

    for field in fields:
        wireFile = open("wires/wires-{}".format(field), "r")
        exWireFile = open("wires/expanded-wires-{}".format(field), "r")
        timingFile = open("encode-timing-new-{}".format(field), "w")
    
        ogWires = wireFile.readlines()
        wireFile.close()
        ogTimeSum = 0
        for i in range(loopCount):
            start_time = time.time()
            encodeWire(ogWires, key)
            ogTimeSum += time.time() - start_time
        timingFile.write("\nEncoding wires of original circuit {}\n".format(ogTimeSum/loopCount))
        print("\nEncoding wires of original circuit {}\n".format(ogTimeSum/loopCount))
        exWires = exWireFile.readlines()
        exWireFile.close()
        exTimeSum = 0
        for i in range(loopCount):
            start_time = time.time()
            encodeWire(exWires, key)
            exTimeSum += time.time()-start_time
        timingFile.write("\nEncoding wires of expanded circuit {}\n".format(exTimeSum/loopCount))
        print("\nEncoding wires of expanded circuit {}\n".format(exTimeSum/loopCount))
        timingFile.close()

main()
