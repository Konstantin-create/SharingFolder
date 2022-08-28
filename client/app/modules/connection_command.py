import sys
import json
import socket
from rich import print


class Connection:
    __slots__ = ('ip', 'hostname', 'port', 'conn', 'token')

    def __init__(self, ip: str, port: int = 8888):
        self.ip = ip
        self.port = port
        self.hostname = socket.gethostname()
        self.conn = None
        self.token = ''

    def is_authorized(self) -> bool:
        """Check is user authorized"""

        if not self.token:
            return False
        return True  # todo token validation

    def post(self, url: str, package: dict) -> dict:
        """Function to send post request"""

        print(bytes(json.dumps(package), encoding="utf-8"))
        package['url'] = url
        self.conn.sendall(bytes(json.dumps(package), encoding="utf-8"))
        response = json.loads(self.conn.recv(3072).decode('utf-8'))
        if not response or response['code'] == 400:
            print('[red]An server error occurred. Try next time later[/red]')
            sys.exit()
        return response

    def start(self):
        """Function to start connection"""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            self.conn.connect((self.ip, self.port))
            self.login()

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
        self.post('/get_hashes', {'token': self.token})
