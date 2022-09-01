import json
import socket
from rich import print
from datetime import datetime
from ..tools import clear_screen, parse_package, generate_key
from ..tools import get_file_hashes


class Server:
    __slots__ = ('working_dir', 'HOST', 'PORT', 'conn', 'addr', 'token')

    def __init__(self, working_dir: str, host: str = '0.0.0.0', port: int = 8888):
        self.working_dir = working_dir
        self.HOST = host
        self.PORT = port
        self.conn = None
        self.addr = ()
        self.token = ''

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
                    data = self.conn.recv(3072).decode()
                    if data:
                        self.router(data)

    def router(self, data) -> None:
        """Function to parse data and routing packages"""

        package = parse_package(data)
        if not package:
            self.conn.send(bytes(json.dumps({'code': 400}), encoding='utf-8'))
        if package['url'] == '/login':
            self.login_route(package)
        elif package['url'] == '/get_hashes':
            self.get_hashes_route(package=package)

    def login_route(self, package: dict):
        """Function of login route"""

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
        self.token = key
        response = {'code': 200, 'token': key}
        self.conn.send(bytes(json.dumps(response), encoding='utf-8'))

    def get_hashes_route(self, package: dict):
        """Function to get current hashes"""

        print(package)
        self.conn.send(bytes(json.dumps(get_file_hashes(self.working_dir)), encoding='utf-8'))
