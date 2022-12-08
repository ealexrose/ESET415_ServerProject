import hashlib
import os
#import tqdm

# This is udpclient.py file

#Import socket programming module
import socket
import pickle
from Knapsack import encrypt, decrypt, knapSum
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Set destination port
port = 65433

# Include the server Address 
serverAddr = ('127.0.0.1', port)

seperator = "<SEPARATOR>"

bufferSize = 4096


#get the file for the csv, confirm that it exists
absolutePath = os.path.dirname(__file__)
relativePath = "FileBin"
fullPath = os.path.join(absolutePath,relativePath)
#fileName = "lab10_test_data-2.csv"

superincreasing = [2, 7, 11, 21, 42, 89, 180, 354]
n = 588
m = 881
inverseModulus = pow(n,-1,m)
clientPublicKey =[]
for i in range(len(superincreasing)):
    clientPublicKey.append((superincreasing[i] * n) % m)
print("Sending key on port " + str(port) + '\n')    
clientPublicKey_bin = pickle.dumps(clientPublicKey)
print(clientPublicKey_bin)
s.sendto(clientPublicKey_bin, serverAddr)
print("Sent client's public key\n")
msg, addr = s.recvfrom(bufferSize)
print(addr)
serverPublicKey_bin = msg
print("Server's public key received: ", serverPublicKey_bin)
serverPublicKey = pickle.loads(serverPublicKey_bin)
print("Server's public key list:", serverPublicKey)


def SendEncrypted(messageToSend):
    encryptedMessage = encrypt(messageToSend,serverPublicKey)
    encryptedMessage_bin = pickle.dumps(encryptedMessage)
    s.sendto(encryptedMessage_bin, addr)

def RecvEncrypted():
    data, addr = s.recvfrom(bufferSize)
    decryptedMessage_bin = pickle.loads(data)
    decryptedMessage = decrypt(decryptedMessage_bin, superincreasing, m, inverseModulus)
    return decryptedMessage, addr

def PutFile(fileName):
    filePath = os.path.join(fullPath,fileName)
    fileExists = False
    if(os.path.exists(filePath)):

        fo = open(filePath,"rb")
        data = fo.read()
        #check hash
        hash_object = hashlib.sha384(data)
        hash_digest = hash_object.hexdigest()

        print(f"\n checksum is\n {hash_digest}\n")
        fo.close()

        fileSize = os.path.getsize(filePath)       
        print(f"Starting upload of {fileName} with a size off {fileSize}")
        fileExists = True
    else:
        print(f"{fileName}does not exist or cannot be found")
        return
    
    #Send Header Data
    if(fileExists):
        #Initial Command (0)
        s.sendto("UploadToServer".encode(),serverAddr)
        #Send name of uploaded file (1)
        s.sendto(f"{fileName}{seperator}{fileSize}{seperator}{hash_digest}".encode(),serverAddr)
    else:
        print("File does not exist or cannot be found")
        return
    #Get acknowledgement that setup is complete (2)
    s.recvfrom(bufferSize)

    #progress = tqdm.tqdm(range(fileSize), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(filePath, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(bufferSize)
            if not bytes_read:
                # file transmitting is done
                break
            # busy networks (3)
            s.sendto(bytes_read,serverAddr)
            #progress.update(len(bytes_read))
            
            # get confirmation that message was received (4)
            s.recvfrom(bufferSize)
    print("Transfer complete")

def GetFile(fileName):

    print(f"Requesting file {fileName} from the server")
    #Send Header Data
    #Initial Command (0)
    s.sendto("DownloadFromServer".encode(),serverAddr)
    #Send name of requested File (1)
    SendEncrypted(f"{fileName}".encode())
    #s.sendto(f"{fileName}".encode(),serverAddr)

    #recieve Header Data, file name and file size from server (2)
    headerBinary, addr = s.recvfrom(bufferSize)
    headerInfo = headerBinary.decode()
    fileName, fileSize, fileHash = headerInfo.split(seperator)
    
    if(int(fileSize) == -1):
        print(f"Server does not contain requested file {fileName}")
        return

    print(f"Recieving {fileName} size of {fileSize}")
    filePath = os.path.join(fullPath,fileName)
    writtenFileSize = 0

    #send acknowledgement that setup is complete (3)
    s.sendto("recieved".encode(), addr)

    #progress = tqdm.tqdm(range(int(fileSize)), f"Recieving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(filePath, "wb") as f:
        while True:
            # read bufferSize bytes from the socket (4)
            bytes_read, addr = s.recvfrom(bufferSize)

            # write to the file the bytes we just received
            f.write(bytes_read)
            
            writtenFileSize = writtenFileSize + len(bytes_read)
            
            #send acknowledgement (5)
            s.sendto(f"buffer received{writtenFileSize}".encode(),serverAddr)
            
            # progress.update(len(bytes_read))
            if writtenFileSize >= int(fileSize):    
                # nothing is received
                # file transmitting is done
                fileSize = os.path.getsize(filePath)
                print(f"Download Completed of {fileName} size on disk is {fileSize} \n")
                f.close()

                fo = open(filePath, "rb")
                data = fo.read()
                #check hash
                hash_object = hashlib.sha384(data)
                hash_digest = hash_object.hexdigest()

                if(hash_digest == fileHash):
                    print(f"{hash_digest}\nhashes match\n")
                else:
                    print(f"{hash_digest}\n!!hash mismatch!!\n")
                fo.close()

                break    



while True:
    cmd = input('Enter a command\n')
    if(len(cmd.split(' ')) == 2):    
        instruction  = cmd.split(' ')[0].lower()
        argument = cmd.split(' ')[1]
    else:
        instruction = cmd
        argument = " "
    
    if(instruction == "help"):
        print("==========================HELP MENU==============================\n")
        print("help - lists available commands\n")
        print("get [filename] - attempts to retrive a file from the server\n")
        print("put [filename] - attempts to upload a file to the server\n")
        print("=================================================================\n")
    elif(instruction == "get"):
        GetFile(argument)
    elif(instruction == "put"):
        PutFile(argument)
    else:
        print("command matches no known instruction, type help for a list of commands\n")




