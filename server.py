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
server.listen()

#Check whether connection is established
curConn, incAddress = server.accept()
with curConn:
  print('Connected with: ', incAddress)
  while True:
    data = curConn.receiver(1024)
    if not data:
      break
     curConn.sendall(data)

def cpu_usage():
  

def processlist():
   
def services():
    
  
