import os


class Host:
    def __init__(self, hostname: str = ''):
        self.host_name = hostname or f'{os.getlogin()}'

    def run(self, port: 8888):
        pass


host = Host()
