# This is udpserver.py file
import socket

# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "10.10.10.12"                          

# Set port number for this server
port = 13000                                          

# Bind to the port
serversocket.bind((ip, port))                                  

def polyEncrypt(message, key):
    index = 0
    newMessage = ""
    for c in message :
        asciiValMessage = ord(c)
        asciiValKey =   ord(key[index])
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

#encrypted = polyEncrypt("spring","dlwfdl")
#print(encrypted)
#print(polyDecrypt(encrypted,"dlwfdl")
key = "dlwf"

def encrypt(plainText):
    cipherReturn = ""
    for s in plainText:
        asciiVal = ord(s)
        asciiVal = (asciiVal + 3) % 128
        cipherReturn = cipherReturn + chr(asciiVal)
    return cipherReturn

def decrypt(plainText):
    cipherReturn = ""
    for s in plainText:
        asciiVal = ord(s)
        asciiVal = (asciiVal + 125) % 128
        cipherReturn = cipherReturn + chr(asciiVal)
    return cipherReturn


while True:  
   print("Waiting to receive a key from port " + str(port) + '\n')   
   # Receive the data of 1024 bytes maximum. 
   data, addr = serversocket.recvfrom(1024)
   key = data.decode()
   print("received Key: " + data.decode())
   
   print("Waiting on message from port " + str(port) + '\n')
   # Receive the data of 1024 bytes maximum. 
   data, addr = serversocket.recvfrom(1024)
   print("reciieved encrypted message : " + data.decode())
   print("received: " + polyDecrypt(data.decode(),key))

   print("send a reply")
   message = input("->")
   encryptedMessage = polyEncrypt(message, key)
   
   #msg = data.decode()
   print(message + " has been encrypted to " + encryptedMessage)
   
   sent = serversocket.sendto(encryptedMessage.encode(), addr)
   print('sent ' + encryptedMessage)




