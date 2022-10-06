import os

# This is udpserver.py file
import socket                                         

# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "127.0.0.1"                          

# Set port number for this server
port = 65432                                          


seperator = "<SEPARATOR>"
bufferSize = 4096

# Bind to the port
serversocket.bind((ip, port))


for i in [1]:  
   print("Waiting to receive file on port " + str(port) + '\n')
   
   # Receive the data of 4096 bytes maximum. Need to use recvfrom because there is not connecction
   data, addr = serversocket.recvfrom(bufferSize)
   receivedPacket = data.decode()
   fileName, fileSize = receivedPacket.split(seperator)

   absolutePath = os.path.dirname(__file__)
   relativePath = "FileBin"
   fullPath = os.path.join(absolutePath,relativePath)
   filePath = os.path.join(fullPath,fileName)
   writtenFileSize = 0
   with open(filePath, "wb") as f:
    while True:
        # read bufferSize bytes from the socket (receive)
        bytes_read, addr = serversocket.recvfrom(bufferSize)

        # write to the file the bytes we just received
        f.write(bytes_read)
        
        writtenFileSize = writtenFileSize + bufferSize
        if writtenFileSize >= int(fileSize):    
            # nothing is received
            # file transmitting is done
            
            print("finished")
            break        

   # close the client socket
   serversocket.close()

