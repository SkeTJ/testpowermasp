import os
import socket

import kivy
import kivymd
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen

KV = '''
MDScreen:
    MDRectangleFlatButton:
        text: "Start Server"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: app.StartServer()

    MDLabel:
        id: statusLabel
        text: "Status"
        font_size: '22.5sp'
        halign: 'center'
        size_hint_y: None
        height: self.texture_size[1]
        padding_y: "250dp"
'''

class Main(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def StartServer(self):
        #Server IP and Port
        HOST = '127.0.0.1' #Temporary localhost for testing (Make sure to use the client's IP during production
        PORT = 21420

        #Start server with the given host and port given and listen for a client
        server = socket.socket()
        server.bind((HOST,PORT))
        print('Server started!')

        #A max of one client can be listend at a time   
        server.listen(1)
        #print('Listening for a client connection to be established...')

        #Check whether connection is established
        curConn, incAddress = server.accept()
        self.root.ids.statusLabel.text = 'A client connected!'
        print('A client has established connection!')

#Juls shizzle
#This is to gather the client's information about their network
def NetworkInfo():
  while True:
    #Send command to the client
    command = 'ipconfig /all'
    command = command.encode()
    currConn.send(command)
    print('Command sent to client: ', command)
    
    #Receive the output given from the client
    output = client.recv(8096)
    output = output.decode()
    print('Output: ', output)
    break

    
#Zees stuff
def cpuusage():
    while True:
        command = 'wmic path Win32_PerfFormattedData_PerfProc_Process get Name,PercentProcessorTime,IDProcess'
        command = command.encode()
        currConn.send(command)
        print('Command sent to client: ', command)
        
        output = client.recv(8096)
        output = output.decode()
        print('Output: ', output)
        break

def tasks():
    while True:
        #send command to client
        command = 'tasklist'
        command = command.encode()
        currConn.send(command)
        print('Command sent to client: ', command)
        
        #receive output from client
        output = client.recv(8096) #tajul is this enough for tasklist?
        output = output.decode()
        print('Output: ', output)
        break

def services():
    while True:
        command = 'net start'
        command = command.encode()
        currConn.send(command)
        print('Command sent to client: ', command)
        
        output = client.recv(8096)
        output = output.decode()
        print('Output: ', output)
        break
        
def killtask():
    while True:
        procname = input('Enter Process Name: ')
        command = 'taskkill /im' + procname
        command = command.encode()
        currConn.send(command)
        print('Command sent to client: ', command)
        
        output = client.recv(8096)
        output = output.decode()
        print('Output: ', output)
        break
        
def shutdown():
    while True:
        command = 'shutdown /s'
        command = command.encode()
        currConn.send(command)
        print('Command sent to client: ', command)
        break
        
    
if __name__ == '__main__':
    Main().run()
