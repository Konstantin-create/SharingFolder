import sys
import json
import socket
import requests
from rich import print


class Connection:
    __slots__ = ('ip', 'hostname', 'port', 'conn', 'token')

    def __init__(self, ip: str, port: int = 8888):
        self.ip = ip
        self.hostname = socket.gethostname()
        self.port = port
        self.conn = None
        self.token = None

    def post(self, url: str, package: dict) -> dict:
        """Function to post package and get json back"""

        try:
            print(str(package))
            return json.loads(requests.post(f'http://{self.ip}:{self.port}/{url}', json=package).text)
        except Exception as e:
            print(f'[red]An error occurred: {e}[/red]')
            sys.exit()

    def is_authorized(self) -> bool:
        """Function to check is user authorized"""

        if self.token:
            response = self.post('is-authorized', {'token': self.token})
            if response['code'] == 200 and response['is_authorized']:
                return True
        return False

    def start(self):
        """Function to start connection"""

        self.login()

    def login(self):
        """Function to log in user"""

        if self.is_authorized():
            pass  # todo
        else:
            response = self.post('login', {"hostname": self.hostname})
            print(response)
            if response['code'] == 200:
                self.token = response['token']
