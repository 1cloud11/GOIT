import socket
import threading
from time import sleep


def start_server(host, port):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        user_socket, address = s.accept()
        print(f'user {address[0]} connected')
        with user_socket:
            while True:
                data = user_socket.recv(2048)
                print(f'Client sent {data.decode("utf-8")}')
                if data.decode("utf-8") == "close":
                    user_socket.send(("Connection is closed.").encode('utf-8'))
                    user_socket.close()
                    break
                user_socket.send(input("Your server message: ").encode('utf-8'))


def start_client(host, port):
    with socket.socket() as s:
        s.connect((host, port))
        while True:
            try:
                s.send(input("Your client message: ").encode('utf-8'))
                data = s.recv(2048)
                print(f'Server sent {data.decode("utf-8")}')
                if data.decode("utf-8") == "Connection is closed.":
                    s.close()
                    break
            except ConnectionAbortedError:
                sleep(0.5)
                print('Anybody home?')


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 1235
    server = threading.Thread(target=start_server, args=(HOST, PORT))
    client = threading.Thread(target=start_client, args=(HOST, PORT))
    server.start()
    client.start()
    server.join()
    client.join()
