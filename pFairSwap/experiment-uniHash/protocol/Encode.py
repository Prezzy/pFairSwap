from protocol.encryption import enc, key_gen
from protocol.merkleTree import makeMerkleTree
import binascii
import argparse



def encodeWire(lines, key):
  
    encWiresWrite = ""
    print("Encrypting wires and creating z...")
    for line in lines:
        chunks = line.split(" ")
        index = chunks[0]
        value = chunks[1].rstrip()
        encWiresWrite += "{}\n".format(enc(int(index), key, int(value, 16)).hex())
    print("last of the encWires{}".format(encWiresWrite[-1]))

    return encWiresWrite




