from web3 import Web3
import math
import binascii

class MerkleTree:
    def __init__(self, data):
        self.dataLen = None
        self.data = None
        self.paddingLen = None
        self.root = None
        self.pad(data)
        self.tree = self.mTree(self.data)
        self.root=self.tree[-1]

    def pad(self, data):
        self.dataLen = len(data)
        targetLength = math.log2(len(data))
        if(targetLength % 1 == 0):
            self.data = data
            self.paddingLen = 0
            return
        paddingLength = int((2**(math.floor(targetLength)+1))) - len(data)
        if(isinstance(data[0], bytes)):
            padding = [bytes([0x00])] * paddingLength
        elif(isinstance(data[0], str)):
            padding = ['0'] * paddingLength
        else:
            print("not bytes or str, reformat")
            return
        data += padding
        self.paddingLen = paddingLength
        self.data = data


    def buildTree(self, root, left, right):
        tree = [root]
        if (isinstance(left, bytes)):
            tree = [right] + tree
            tree = [left] + tree
            return tree

        size = len(left)
        track = -1
        while len(left):
            tree = left[track:] + right[track:] + tree 
            del right[track:]
            del left[track:]
            track = track*2
        return tree

    def mTree(self, arr):
        if len(arr) <=1:
            if(isinstance(arr[0], bytes)):
                val = Web3.keccak(arr[0])
                return val
            elif(isinstance(arr[0], str)):
                val = Web3.keccak(text = arr[0])
                return val

        elif len(arr) >= 2:
            left = self.mTree(arr[:len(arr)//2])
            right = self.mTree(arr[len(arr)//2:])
            if(isinstance(left, bytes)):
                l = left
                r = right
            else: 
                l = left[-1]
                r = right[-1]
            root = Web3.solidityKeccak(['bytes32', 'bytes32'], [l,r])
            return(self.buildTree(root, left, right))

    def mProof(self, i):
        if(self.dataLen-1 < i):
            #print("element at index {} does not exist".format(i))
            return
        element = self.data[i]
        #print("len tree {}".format(len(self.tree)))
        n = (len(self.tree)+1)/2
        #print("n is {}".format(n))
        j = math.floor(math.log2(n))
        #print(j)

        proof = []
        parentIdx = n
        while j > 0:
            #print("val of i {}".format(i))
            if i % 2 == 0:
                proof.append(self.tree[i+1])
                i = int(i + (n -(i/2)))
            else:
                proof.append(self.tree[i-1])
                i = i - 1
                i = int(i + (n -(i/2)))
            parentIdx = int(parentIdx/2)
            j -= 1
        return proof




def mVrfy(idx, element, proof, root):
    if(isinstance(element, bytes)):
        element = Web3.soliditySha3(['bytes32'],[element])
    elif (isinstance(element, str)):
        #print("element in mVrfy - {}".format(element))
        element = Web3.soliditySha3(['string'],[element])
        #print("hash of ele - {}".format(element.hex()))
    for j in range(len(proof)):
        if(idx//2**j)%2 == 0:
            #print("ele / proof {} {}".format(element.hex(), proof[j].hex()))
            element = Web3.soliditySha3(['bytes32','bytes32'], [element, proof[j]])
            #print("element {}: {}".format(j, element.hex()))
        else:
            #print("proof / ele {} {}".format(proof[j].hex(), element.hex()))
            element = Web3.soliditySha3(['bytes32', 'bytes32'], [proof[j], element])
            #print("element {}: {}".format(j, element.hex()))

    if element == root:
        return 1
    else:
        return 0


def main():
    elements = ['1','2','3','4','5']

    merkleTree = MerkleTree(elements)

    proof = merkleTree.mProof(0)

    print(merkleTree.tree)
    print(proof)

    print(mVrfy(0, '1', proof, merkleTree.root))
