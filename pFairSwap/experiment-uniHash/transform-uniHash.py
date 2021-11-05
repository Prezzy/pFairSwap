from protocol.CircuitTransformer import transform

def main():

    fields = [127, 107, 89]

    for field in fields:
        circuitFile = open("circuits/uniHash-{}.arith".format(field), "r")
        circuitLines = circuitFile.readlines()
        circuitFile.close()

        transformedCircuit = transform(circuitLines, (2**field)-1, (field-1)//8)
        transformedCircuitFile = open("circuits/expanded-uniHash-{}.arith".format(field), "w")
        transformedCircuitFile.write(transformedCircuit[1])
        transformedCircuitFile.close()

main()
