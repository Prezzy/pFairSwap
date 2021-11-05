from CircuitTransformer import transform



def main():

    feilds = [127, 107, 89]

    for feild in feilds:
        cirFile = open("uniHash-{}.arith".format(feild), "r")
        lines = cirFile.readlines()
        cirFile.close()
        transformedLines = transform(lines)
        transCirFile = open("trans-uniHash-{}.arith".format(feild), "w")
        transCirFile.write(transformedLines[1])
        transCirFile.close()


main()
