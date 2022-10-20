from dataclasses import dataclass
import os
import tqdm
import hashlib

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


absolutePath = os.path.dirname(__file__)
relativePath = "FileBin"
fullPath = os.path.join(absolutePath,relativePath)

def PutFile():
   print("Waiting to receive an instruction on port " + str(port) + '\n')

   # Receive the data of 4096 bytes maximum. Need to use recvfrom because there is not tcp connecction
   data, addr = serversocket.recvfrom(bufferSize)
   receivedPacket = data.decode()
   fileName, fileSize, fileHash = receivedPacket.split(seperator)
   print(f"\nRecieving {fileName} size of {fileSize}\n hash is {fileHash}\n")
   filePath = os.path.join(fullPath,fileName)
   writtenFileSize = 0
   serversocket.sendto("recieved".encode(), addr)
   progress = tqdm.tqdm(range(int(fileSize)), f"Recieving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
   with open(filePath, "wb") as f:
    while True:
        # read bufferSize bytes from the socket (receive)
        bytes_read, addr = serversocket.recvfrom(bufferSize)

        # write to the file the bytes we just received
        f.write(bytes_read)
        
        writtenFileSize = writtenFileSize + len(bytes_read)
        progress.update(len(bytes_read))
        if writtenFileSize >= int(fileSize):    
            # nothing is received
            # file transmitting is done
            fileSize = os.path.getsize(filePath)
            print(f"Upload Completed of {fileName} size on disk is {fileSize} \n")
            print("finished")
            f.close()
            break
    fo = open(filePath,"rb")
    data = fo.read()

    #check hash
    hash_object = hashlib.sha384(data)
    hash_digest = hash_object.hexdigest()

    if(hash_digest == fileHash):
        print(f"{hash_digest}\nhashes match\n")
    else:
        print(f"{hash_digest}\n!!hash mismatch!!\n")
    fo.close()

def GetFile():
    #Get name of requested file
    data, addr = serversocket.recvfrom(bufferSize)
    fileName = data.decode()

    filePath = os.path.join(fullPath,fileName)
    if(os.path.exists(filePath)):
        fileSize = os.path.getsize(filePath)

        fo = open(filePath,"rb")
        data = fo.read()
        #check hash
        hash_object = hashlib.sha384(data)
        hash_digest = hash_object.hexdigest()
        fo.close()

        #send back file name and file size to client
        print(f"Starting upload of {fileName} with a size off {fileSize}\n hash is\n{hash_digest}")   
        serversocket.sendto(f"{fileName}{seperator}{fileSize}{seperator}{hash_digest}".encode(),addr)
    else:
        print(f"{fileName}does not exist or cannot be found")
        return
    
    #Get acknowledgement that setup is complete
    serversocket.recvfrom(bufferSize)

    progress = tqdm.tqdm(range(fileSize), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(filePath, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(bufferSize)
            if not bytes_read:
                # file transmitting is done
                break
            # busy networks
            serversocket.sendto(bytes_read,addr)
            progress.update(len(bytes_read))
    print("\nTransfer complete\n")
    


while True:
    data, addr = serversocket.recvfrom(bufferSize)
    instruction = data.decode()
    if(instruction == "UploadToServer"):
        PutFile()
    elif(instruction == "DownloadFromServer"):
        GetFile()
    else:
        print(f"Client Header Contained Unrecognized Command{instruction}")

