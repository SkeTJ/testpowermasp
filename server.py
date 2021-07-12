import os
import socket

import kivy
import kivymd
from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
MDScreen:
    MDRectangleFlatButton:
        text: "Network Info"
        pos_hint: {"center_x": .5, "center_y": .5}     
'''

class Main(MDApp):
    def build(self):
        ###Server IP and Port
        HOST = '127.0.0.1' #Temporary localhost for testing (Make sure to use the client's IP during production
        PORT = 21420

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
        
        return Builder.load_string(KV)

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

Main().run()
