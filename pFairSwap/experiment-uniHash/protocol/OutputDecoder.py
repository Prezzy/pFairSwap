import binascii

inFile = open("encoded-outputs","r")
lines = inFile.readlines()

def combineShares(shares):
    secret = 0
    for i in shares:
        print(i)
        secret = pow(secret + int(i,16),1,(2**521)-1)
    return secret


while(lines):
    shares = []
    for i in range(3):
        line = lines.pop(0)
        parsed = line.split(" ")
        shares.append(parsed[1])
    secret = combineShares(shares)
    print("{}".format(secret))
        
