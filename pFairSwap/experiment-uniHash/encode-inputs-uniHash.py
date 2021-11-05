from protocol.InputEncoder import encodeInput

def main():
    fields = [127, 107, 89]

    for field in fields:
        inputsFile = open("inputs/inputs-{}".format(field), "r")
        inputLines = inputsFile.readlines()
        inputsFile.close()

        encodedInputs = encodeInput(inputLines,(2**field)-1,(field-1)//8)
        encodedInputsFile = open("inputs/encoded-inputs-{}".format(field), "w")
        encodedInputsFile.write(encodedInputs)
        encodedInputsFile.close()

main()
