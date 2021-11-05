from protocol.encryption import key_gen

keyFile = open("key", "wb")

key = key_gen(32)

keyFile.write(key)
