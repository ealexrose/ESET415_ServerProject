privateKey = [2, 7, 11, 21, 42, 89, 180, 354]
n = 588
m = 881
publicKey =[295, 592, 301, 14, 28, 353, 120, 236]
inverseM = 442

booleanValue = b'hello'


def encrypt(message, key):
    weightedSums = []
    for i in range(len(message)):
        sum = 0       
        for j  in range(len(key)):
            if ((1<<j) & message[i]) != 0:
                sum += key[7-j]
        weightedSums.append(sum)
    return weightedSums

def knapSum(asciiValue, private_key):
    sum = 0
    for j  in range(8):
        if ((1<<j) & asciiValue) != 0:
            sum += private_key[7-j]
    return sum

def decrypt(message, private_key, mVal, invMVal):
    targetSums = []
    actualValues = []
    
    for i in range(len(message)):
        val = (message[i] * invMVal)  % mVal
        targetSums.append(val)
    for i in range(len(targetSums)):
        for j in range(255):
            asciiVal = knapSum(j, private_key)
            if targetSums[i] == asciiVal:
                actualValues.append(j.to_bytes(1, 'big'))
                break
    return b''.join(actualValues)

result = encrypt(b"test", publicKey)
#print(result)

decryption = decrypt(result, privateKey, m, inverseM)
#print(decryption)