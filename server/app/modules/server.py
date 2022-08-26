import json
import socket
from rich import print
from datetime import datetime
from ..tools import clear_screen, parse_package, generate_key


class Server:
    __slots__ = ('HOST', 'PORT', 'conn', 'addr')

    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.HOST = host
        self.PORT = port
        self.conn = None
        self.addr = ()

    def run(self, accept_all: bool = False):
        """Run function. Start server"""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            clear_screen()
            print('[green] Initialize server[/green]')
            s.listen()
            self.conn, self.addr = s.accept()
            print(f'[yellow] Incoming connection: {self.addr}[/yellow]')

            with self.conn:
                while True:
                    data = self.conn.recv(1024).decode()
                    if not data:
                        break
                    self.router(data)
            s.close()

    def router(self, data) -> None:
        """Function to parse data and routing packages"""

        package = parse_package(data)
        if not package:
            self.conn.sendall(bytes(json.dumps({'code': 400}), encoding='utf-8'))
        if package['url'] == '/login':
            self.login_route(package)

    def login_route(self, package: dict):
        print(str(
            {'ip': self.addr[0],
             'hostname': package['hostname'],
             'time_stamp': str(datetime.utcnow())
             }
        ))
        key = generate_key(
            {'ip': self.addr[0],
             'hostname': package['hostname'],
             'time_stamp': str(datetime.utcnow())
             })
        response = {'code': 200, 'token': key}
        self.conn.sendall(bytes(json.dumps(response), encoding='utf-8'))
