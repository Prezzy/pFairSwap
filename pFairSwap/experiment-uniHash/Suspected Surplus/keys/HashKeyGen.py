import os

def hashKeyGen(numKeys, keySize, name):
    f = open("key-{}".format(name), "w")

    for i in range(numKeys):
        keyi = os.urandom(keySize)
        f.write("{}\n".format(keyi.hex()))

    f.close()

def createKey(feild, numKeys):

    keySize = feild // 8
    hashKeyGen(numKeys, keySize, feild)


def main():

    numKeys = 21
    feilds = [1279, 607, 521, 127, 107, 89]

    for feild in feilds:
        createKey(feild, numKeys)


main()
