
def uniHash(key, msg):

    i = 0
    temp = 0

    while(i < 4):
        j = 0
        temp = temp * key[0]
        print("mul with idx 0 {}".format(temp))
        for j in range(1,2):
            temp += msg[i] * key[j]
            print("add {}".format(temp))
            i += 1


    hashval = temp

    print(hashval)


key = [5,5,5]
msg = [2,2,2,2]
uniHash(key, msg)
