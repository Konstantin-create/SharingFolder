import socket
import sys

from rich import print


class Server:
    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.HOST = host
        self.PORT = port

    def run(self, accept_all: bool = False):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            if not accept_all:
                command = input(f'Accept connection from {addr[0]}:{addr[1]}?\n  Yes/No: ')
                if 'n' in command.lower():
                    conn.close()

            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    print(data)
            s.close()
