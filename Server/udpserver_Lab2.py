from dataclasses import dataclass
import os
#import tqdm
import hashlib
import math
import socket                                         
import pickle
from Knapsack import encrypt, decrypt, knapSum
# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "127.0.0.1"                          

# Set port number for this server
port = 65433                                          


seperator = "<SEPARATOR>"
bufferSize = 4096
# Bind to the port
serversocket.bind((ip, port))

absolutePath = os.path.dirname(__file__)
relativePath = "FileBin"
fullPath = os.path.join(absolutePath,relativePath)





    
superincreasing = [2,3,6,13,27,52,105,210]
n = 249
m = 419
inverseModulus = pow(n,-1,m)
serverPublicKey =[]
for i in range(len(superincreasing)):
    serverPublicKey.append((superincreasing[i] * n) % m)
    
print("Waiting to receive message on port " + str(port) + '\n')
#receive key from client  
data, addr = serversocket.recvfrom(bufferSize)
print(addr)
clientPublicKey_bin = data
print("Client's key received: " , clientPublicKey_bin)
clientPublicKey = pickle.loads(clientPublicKey_bin)
print("Client's public key list:", clientPublicKey)

#send server's public key to client
serverPublicKey_bin = pickle.dumps(serverPublicKey)
print("\n Will send server's public key ", serverPublicKey_bin)
serversocket.sendto(serverPublicKey_bin, addr)
print("Sent server's public key ")

def SendEncrypted(messageToSend):
    encryptedMessage = encrypt(messageToSend,clientPublicKey)
    encryptedMessage_bin = pickle.dumps(encryptedMessage)
    serversocket.sendto(encryptedMessage_bin, addr)

def RecvEncrypted():
    data, addr = serversocket.recvfrom(bufferSize)
    decryptedMessage_bin = pickle.loads(data)
    decryptedMessage = decrypt(decryptedMessage_bin, superincreasing, m, inverseModulus)
    return decryptedMessage, addr

def PutFile():
   print("Waiting to receive an instruction on port " + str(port) + '\n')

   # Receive the data of 4096 bytes maximum. Need to use recvfrom because there is not tcp connecction(1)
   data, addr = RecvEncrypted()
   receivedPacket = data.decode()
   fileName, fileSize, fileHash = receivedPacket.split(seperator)
   print(f"\nRecieving {fileName} size of {fileSize}\n hash is {fileHash}\n")
   filePath = os.path.join(fullPath,fileName)
   writtenFileSize = 0
   
   #confirm initial setup (2)
   SendEncrypted("recieved".encode())
   #progress = tqdm.tqdm(range(int(fileSize)), f"Recieving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
   with open(filePath, "wb") as f:
    while True:
        # read bufferSize bytes from the socket (3)
        bytes_read, addr = RecvEncrypted()

        # write to the file the bytes we just received
        f.write(bytes_read)
        
        writtenFileSize = writtenFileSize + len(bytes_read)
        #send received signal (4)
        SendEncrypted("recieved".encode())
        
        #progress.update(len(bytes_read))
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
    #Get name of requested file (1)
    data, addr = RecvEncrypted() #serversocket.recvfrom(bufferSize)
    
# =============================================================================
#     test = data
#     test = encrypt(test, serverPublicKey)
#     test = decrypt(test, superincreasing, m, inverseModulus)
#     test = test.decode()
#     print(test)
# =============================================================================
    
    fileName = data.decode()
    
    filePath = os.path.join(fullPath,fileName)
    
    #if the file exists, get the file size, open it, and get the file hash
    if(os.path.exists(filePath)):
        
        fileSize = os.path.getsize(filePath)
        fo = open(filePath,"rb")
        data = fo.read()
        
        #check hash
        hash_object = hashlib.sha384(data)
        hash_digest = hash_object.hexdigest()
        fo.close()

        #send back file name, size, and hash to client (2)
        print(f"Starting upload of {fileName} with a size off {fileSize}\n hash is\n{hash_digest}")   
        SendEncrypted(f"{fileName}{seperator}{fileSize}{seperator}{hash_digest}".encode())
        
    else:
        #send back error (2)
        print(f"{fileName} does not exist or cannot be found")  
        SendEncrypted(f"{fileName}{seperator}-1{seperator}-1".encode())
        
        return
    
    #Get acknowledgement that setup is complete (3)
    RecvEncrypted()
    
    #progress = tqdm.tqdm(range(fileSize), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(filePath, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(1024)
            if not bytes_read:
                # file transmitting is done
                break
            # busy networks (4)
            SendEncrypted(bytes_read)
            #progress.update(len(bytes_read))
            
            #Get acknowledgement that buffer was received (5)
            RecvEncrypted()
    print("\nTransfer complete\n")




while True:
    data, addr = serversocket.recvfrom(bufferSize)
    instruction = data.decode()
    #get the kind of instruction (0)
    if(instruction == "UploadToServer"):
        PutFile()
    elif(instruction == "DownloadFromServer"):
        GetFile()
    else:
        print(f"Client Header Contained Unrecognized Command{instruction}")

