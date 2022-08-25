import socket
from rich import print
from ..tools import clear_screen, parse_package


class Server:
    __slots__ = ('HOST', 'PORT', 'conn', 'addr')

    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.HOST = host
        self.PORT = port
        self.conn = None
        self.addr = ()

    def run(self, accept_all: bool = False):
        """Run function. Start server"""

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.HOST, self.PORT))
                clear_screen()
                print('[green] Initialize server[/green]')
                s.listen()
                self.conn, self.addr = s.accept()
                print(f'[yellow] Incoming connection: {self.addr}[/yellow]')
                if not accept_all:
                    command = input(f'Accept connection from {self.addr[0]}:{self.addr[1]}?\n  Yes/No: ')
                    if 'n' in command.lower():
                        self.conn.close()
                        clear_screen()
                        continue

                with self.conn:
                    clear_screen()
                    print(f'[green] Shared with {self.addr[0]}[/green]')
                    while True:
                        data = self.conn.recv(1024).decode()
                        if not data:
                            break
                        self.router(data)
                s.close()

    def router(self, data) -> None:
        """Function to parse data and routing packages"""

        package = parse_package(data)
        print(package['url'] == '/login')
        if package['url'] == '/login':
            self.login_route(package)

    def login_route(self, package: dict):
        if 'json' not in package:
            self.conn.send(str({'code': 400}).encode())
            self.conn.close()
            return
        self.conn.send(str({'code': 200, 'token': 'fadjnadsdneo'}).encode())
