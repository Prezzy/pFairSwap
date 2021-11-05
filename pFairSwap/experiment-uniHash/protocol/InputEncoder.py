import os
import binascii
import argparse
from protocol.SecretShare import genSecretShares




def encodeInput(lines, P, byteSize):
    wireId = 0
    outFileWrite = ""
    tracker = 0

    for line in lines:
        print(tracker)
        tracker += 1
        parsed = line.split(" ")
        inVal = int(parsed[1],16)
        shares = genSecretShares(inVal, P, byteSize)
        for i in shares:
            outFileWrite += "{} {}\n".format(wireId, i)
            wireId += 1
        print(shares)



    outFileWrite += "{} {}\n".format(wireId, 1)

    return outFileWrite
