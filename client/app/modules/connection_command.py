import sys
import json
import time
import socket
from rich import print
from datetime import datetime

from ..tools import *


class Connection:
    __slots__ = ('ip', 'hostname', 'port', 'conn', 'token', 'server_structure', 'last_get_structure_request')

    def __init__(self, ip: str, port: int = 8888):
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
        return True  # todo token validation

    def post(self, url: str, package: dict) -> dict:
        """Function to send post request"""

        package['url'] = url
        self.conn.sendall(bytes(json.dumps(package), encoding="utf-8"))
        response = json.loads(self.conn.recv(3072).decode('utf-8'))
        if not response or response['code'] == 400:
            print('[red]An server error occurred. Try next time later[/red]')
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
        self.server_structure = self.post('/get_hashes', {'token': self.token})
        # self.compare_structures()
        print(self.server_structure)
        sys.exit()

    def compare_structures(self):
        """Function to compare local folder structure and server folder structure"""

        local_structure = None
