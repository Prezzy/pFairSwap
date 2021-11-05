from Encode import encodeWire
from encryption import key_gen

def main():

    feilds = [127, 107, 89]

    key = key_gen(16)

    for feild in feilds:
        wireFile = open("wires-{}".format(feild), "r")

        wires = wireFile.readlines()
        wireFile.close()
        encWires = encodeWire(wires, key)
        encFile = open("enc-wires-{}".format(feild), "r")
        encFile.close()

main()
