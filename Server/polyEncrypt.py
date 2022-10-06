def polyEncrypt(message, key):
    index = 0
    newMessage = ""
    for c in message :
        asciiValMessage = ord(c)
        asciiValKey =ord(key[index])
        encryptedValue = (asciiValMessage + asciiValKey) % 128
        newChar = chr(encryptedValue)
        newMessage += newChar
        index = (index + 1) % len(key)
    return newMessage

def polyDecrypt(message, key):
    index = 0
    newMessage = ""
    for c in message :
        asciiValMessage = ord(c)
        asciiValKey =ord(key[index])
        encryptedValue = (asciiValMessage + (128 - asciiValKey)) % 128
        newChar = chr(encryptedValue)
        newMessage += newChar
        index = (index + 1) % len(key)
    return newMessage

encrypted = polyEncrypt("Eset 415 classes are on Mondays and Wednesdays","dlwf")
print("encrypting Eset 415 classes are on Mondays and Wednesdays using key dlwf \n")
print(encrypted)
print(polyDecrypt(encrypted,"dlwf"))
