# This is udpserver.py file
import socket                                         

# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "10.228.55.39"                          

# Set port number for this server
port = 13000                                          

# Bind to the port
serversocket.bind((ip, port))                                  

while True:  
   print("Waiting to receive message on port " + str(port) + '\n')
   
   # Receive the data of 1024 bytes maximum. Need to use recvfrom because there is not connecction
   data, addr = serversocket.recvfrom(1024)
   print("received: " + data.decode())

   print("send a reply")    
   msg = data.decode()
   print(msg)
   sent = serversocket.sendto(msg.encode(), addr)
   print('sent ' + str(sent))
