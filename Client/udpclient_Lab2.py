import os

# This is udpclient.py file

#Import socket programming module
import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Set destination port
port = 65432

# Include the server Address 
serverAddr = ('127.0.0.1', port)

seperator = "<SEPARATOR>"
bufferSize = 4096


#get the file for the csv, confirm that it exists
absolutePath = os.path.dirname(__file__)
relativePath = "FileBin"
fullPath = os.path.join(absolutePath,relativePath)
fileName = "lab10_test_data-2.csv"

filePath = os.path.join(fullPath,fileName)
fileSize = os.path.getsize(filePath)
print(fileSize)

# Send message. The string needs to be converted to bytes.
# To send more than one message, please create a loop
print("Type anything to send the hardcoded file")
message = input("->")
#s.sendto(message.encode(), serverAddr)
s.sendto(f"{fileName}{seperator}{fileSize}".encode(),serverAddr)

with open(filePath, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(bufferSize)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendto(bytes_read,serverAddr)
# close the socket
s.close()
print("Transfer complete")
