import socket
from rich import print
from ..tools import clear_screen


class Server:
    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.HOST = host
        self.PORT = port

    def run(self, accept_all: bool = False):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.HOST, self.PORT))
                print('[green] Initialize server[/green]')
                s.listen()
                conn, addr = s.accept()
                print(f'[yellow] Incoming connection: {addr}[/yellow]')
                if not accept_all:
                    command = input(f'Accept connection from {addr[0]}:{addr[1]}?\n  Yes/No: ')
                    if 'n' in command.lower():
                        conn.close()
                        clear_screen()
                        continue

                with conn:
                    clear_screen()
                    print(f'[green] Shared with {addr[0]}[/green]')
                    while True:
                        data = conn.recv(1024).decode()
                        if not data:
                            break
                        print(data)
                s.close()
