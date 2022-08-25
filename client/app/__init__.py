import sys
from rich import print

from .tools import *
from .tools.help_tools import *

from .modules import *

args = sys.argv


def main():
    if len(args) <= 1 or args[1] == '-h' or args[1] == '--help':
        print(global_help)
        return
    if args[1] == 'connect':
        if len(args) < 3:
            print('[red]Not enough arguments[/red]')
            print(connect_help)
            return
        if '-i' in args or '--ip' in args:
            if '-i' in args:
                ip_flag = '-i'
            else:
                ip_flag = '--ip'
            if len(args) < args.index(ip_flag) + 1:
                print('[red]Argument error. Ip field not found[/red]')
                return
            ip = args[args.index(ip_flag) + 1]
            if not check_ip(ip):
                print(f'[red]Ip {ip} is not exists[/red]')
                return
            connection = Connection(ip)
            connection.start()


main()
