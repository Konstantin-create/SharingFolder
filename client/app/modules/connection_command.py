import os
import sys
import json
import time
import socket
from rich import print
from datetime import datetime

from ..tools import *


class Connection:
    __slots__ = (
        'ip', 'hostname', 'port',
        'conn', 'token', 'server_structure',
        'last_get_structure_request', 'working_dir', 'root_folder'
    )

    def __init__(self, working_dir: str, ip: str, port: int = 8888):
        self.working_dir = working_dir  # Field to save current working dir
        self.root_folder = ''  # Field to save server name folder

        self.ip = ip  # Field to saver server ip
        self.port = port  # Field to save server port
        self.hostname = socket.gethostname()  # Field to save client hostname
        self.conn = None  # Field to save current connection
        self.token = ''  # Field to save token to access server
        self.server_structure = []  # Field to save sharing folder structure
        self.last_get_structure_request = datetime.utcnow()  # Field to save last request to server on get structure url

    def is_authorized(self) -> bool:
        """Check is user authorized"""

        if not self.token:
            return False
        return True

    def post(self, url: str, package: dict) -> dict:
        """Function to send post request"""

        package['url'] = url
        self.conn.sendall(bytes(json.dumps(package), encoding="utf-8"))
        response = json.loads(self.conn.recv(3072).decode('utf-8'))

        # Response errors handlers
        if not response or response['code'] == 400:
            print('[red]An server error occurred. Try next time later[/red]')
            self.conn.close()
            sys.exit()
        elif response['code'] == 600:
            print('[red]Authorization error(token is not valid)[/red]')
            self.conn.close()
            sys.exit()
        self.conn.close()
        return response

    def start(self):
        """Function to start connection"""

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
                self.conn.connect((self.ip, self.port))
                self.login()
                time.sleep(0.5)

    def login(self):
        """Login function"""

        if self.is_authorized():
            self.get_hashes()
        self.token = self.post('/login', {'hostname': self.hostname})['token']

    def get_hashes(self):
        """Get files hashes functions"""

        if not self.is_authorized():
            self.login()
            return
        response = self.post('/get_hashes', {'token': self.token})
        self.server_structure = response['hashes']
        self.root_folder = response['root_folder']
        self.compare_structures()
        # print(response)
        sys.exit()

    def compare_structures(self):
        """Function to compare local folder structure and server folder structure"""

        local_structure = get_file_hashes(self.working_dir, self.root_folder)
        if not local_structure:
            print(f'[yellow]Folder "{self.root_folder}" not found. Copy from server? Yes/no:[/yellow]')
            command = input('~ ')
            if 'n' in command:
                print('Closing the connection...')
                self.conn.close()
                sys.exit()
            if not os.path.exists(f'{self.working_dir}/{self.root_folder}'):
                os.mkdir(f'{self.working_dir}/{self.root_folder}')
            # todo: copy tree from server
        else:
            print(get_file_hashes())
        print(local_structure)
