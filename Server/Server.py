# This is udpserver.py file
import socket

# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "20.20.20.6"                          

# Set port number for this server
port = 13000                                          

# Bind to the port
serversocket.bind((ip, port))                                  

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
   print("Waiting to receive message on port " + str(port) + '\n')
   
   # Receive the data of 1024 bytes maximum. 
   data, addr = serversocket.recvfrom(1024)
   print("received: " + decrypt(data.decode()))
   print("send a reply")
   message = input("->")
   encryptedMessage = encrypt(message)
   
   #msg = data.decode()
   print(message + " has been encrypted to " + encryptedMessage)
   
   sent = serversocket.sendto(encryptedMessage.encode(), addr)
   print('sent ' + encryptedMessage)




