import os
#inputFile = open("ajtai-inputs", "w")


msg = "This is the message you want"
binString = ""
for c in msg:
    ascii_val = ord(c)

    binary_val = bin(ascii_val)

    binString += binary_val[2:]

padding = "0" * (2500 - len(binString))

binString += padding


def getPaddedBinString(msg, MSIZE):
    binString = ""
    for c in msg:
        asciiVal = ord(c)
        binaryVal = bin(ascii_val)
        binString += binary_val[2:]

    padding = "0" * (MSIZE - len(binString))
    binString += padding

    return binString

   
def writeInputFile(inputFile, binString, MSIZE, NSIZE):

    for i in range(MSIZE):
        inputFile.write("{} 0x{}\n".format(i, binString[i]))

    for i in range(MSIZE, (MSIZE*NSIZE)+MSIZE):
        randomVal = os.urandom(16)
        inputFile.write("{} 0x{}\n".format(i, randomVal.hex()))

    inputFile.write("{} 0x1".format(MSIZE*NSIZE + MSIZE))


