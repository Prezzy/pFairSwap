from protocol.InputEncoder import encodeInput
from protocol.CircuitTransformer import transform

inputFile = open("inputs/inputs-89", "r")
inputLines = inputFile.readlines()
testEncodeFile = open("encoded-inputs-89", "w")

circuitFile = open("circuits/uniHash-89.arith", "r")
exCirFile = open("expanded-uniHash-89.arith", "w")
circuitLines = circuitFile.readlines()

expandedCirLines = transform(circuitLines, (2**89)-1, (89-1)//8)

exCirFile.write(expandedCirLines[1])

testLines = encodeInput(inputLines, (2**89)-1, (89-1)//8)

testEncodeFile.write(testLines)
