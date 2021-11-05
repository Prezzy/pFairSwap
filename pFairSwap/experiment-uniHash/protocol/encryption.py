from web3 import Web3
from os import urandom

def key_gen(num_bytes):
    return urandom(num_bytes)



def enc(index, key, plaintext):
    key_i_hash = Web3.soliditySha3(['bytes32', 'uint256'], [key, index])
    if(index == 5100):
        print("key Hash for 5100 {}".format(key_i_hash.hex()))
    if(isinstance(plaintext, bytes)):
        plaintext = int.from_bytes(plaintext, "big")
    key_i_hash = int.from_bytes(key_i_hash, "big")
    cipherInt = plaintext ^ key_i_hash
    return cipherInt.to_bytes(32, "big")




def dec(index, key, ciphertext):
    key_i_hash = Web3.soliditySha3(['bytes32','uint256'], [key, index])
    print("key_i - {}".format(key_i_hash.hex()))
    if(isinstance(ciphertext, bytes)):
        ciphertext = int.from_bytes(ciphertext, "big")
    plainInt = ciphertext ^ int.from_bytes(key_i_hash, "big")

    return plainInt.to_bytes(32, "big")




