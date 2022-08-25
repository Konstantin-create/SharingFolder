import socket


class Connection:
    __slots__ = ('ip', 'hostname')

    def __init__(self, ip: str):
        self.ip = ip
        self.hostname = socket.gethostname()

    def start(self):
        """Function to start connection"""

        print(self.ip)
        print(self.hostname)
