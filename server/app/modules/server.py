import json
import socket
from rich import print
from datetime import datetime
from ..tools import clear_screen, parse_package, generate_key
from ..tools import get_file_hashes


class Server:
    __slots__ = ('working_dir', 'root_folder', 'HOST', 'PORT', 'conn', 'addr', 'token')

    def __init__(self, working_dir: str, host: str = '0.0.0.0', port: int = 8888):
        # File system constants
        self.working_dir = working_dir
        self.root_folder = working_dir[working_dir.rfind('/') + 1:]

        # Server constants
        self.HOST = host
        self.PORT = port

        # Connection variables
        self.conn = None
        self.addr = ()
        self.token = ''

    def token_validation(self, package: dict):
        """Function to validate token"""

        if not self.token or 'token' not in package or package['token'] != self.token:
            return False
        return True

    def run(self, accept_all: bool = False):
        """Run function. Start server"""

        clear_screen()
        print('[green] Initialize server[/green]')
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.HOST, self.PORT))
                s.listen()
                self.conn, self.addr = s.accept()

                with self.conn:
                    while True:
                        data = self.conn.recv(3072).decode()
                        if not data:
                            break
                        self.router(data)
                    self.conn.close()

    def router(self, data) -> None:
        """Function to parse data and routing packages"""

        package = parse_package(data)
        if not package:
            self.conn.sendall(bytes(json.dumps({'code': 400}), encoding='utf-8'))
        print(f'[yellow] Incoming package: {self.addr}[/yellow] {package["url"]}')
        if package['url'] == '/login':
            self.login_route(package)
        elif package['url'] == '/get_hashes':
            self.get_hashes_route(package=package)

    def login_route(self, package: dict):
        """Function of login route"""

        key = generate_key(
            {'ip': self.addr[0],
             'hostname': package['hostname'],
             'time_stamp': str(datetime.utcnow())
             })
        self.token = key
        response = {'code': 200, 'token': key}
        self.conn.sendall(bytes(json.dumps(response), encoding='utf-8'))

    def get_hashes_route(self, package: dict):
        """Function to get current hashes"""

        if not self.token_validation(package):
            self.conn.sendall(bytes(json.dumps({
                'code': 600
            }), encoding='utf-8'))

        file_hashes = get_file_hashes(self.working_dir)
        if not file_hashes:
            self.conn.sendall(bytes(json.dumps({
                'code': 500
            }), encoding='utf-8'))
            return
        self.conn.sendall(
            bytes(json.dumps({
                'code': 200,
                'hashes': file_hashes,
                'root_folder': self.root_folder
            }), encoding='utf-8')
        )
