import os
import socket
import tkinter as tk
import kivy #owo
import wmi

#ngl i think using kivy would be more ni1cer for the ui than tkinter coz it looks more modern, besides,
#its wat i use for ma fyp too :D -jul sux hehehe omg, its u (only old ppl know this reference)
#master programmer, use what you want. imma just do the functions that i was ASSigned

#Server IP and Port
HOST = '127.0.0.1' #Temporary localhost for testing (Make sure to use the client's IP during production
PORT = 69420

#Start server with the given host and port given and listen for a client
server = socket.socket()
server.bind((HOST,PORT))
print('Server started!')

#A max of one client can be listend at a time
server.listen(1)
print('Listening for a client connection to be established...')

#Check whether connection is established
curConn, incAddress = server.accept()
print('A client has established connection!')

#Juls shizzle
#This is to gather the client's information about their network
def NetworkInfo():
  while True:
    #Send command to the client
    command = 'ipoconfig /all'
    command = command.encode()
    currConn.send(command)
    print('Command sent to client: ', command)
    
    #Receive the output given from the client
    output = client.recv(8096)
    output = output.decode()
    print('Output: ', output)
    break

#Zees shizzle
def cpu_usage():
  
def processlist():
   
def services():
    
  
