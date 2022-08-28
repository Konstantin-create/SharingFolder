import os
import sys
from rich import print
from .modules import server
from .tools import help_tools

args = sys.argv


def main():
    cwd = os.getcwd()
    if len(args) < 2:
        print(help_tools.global_help)
        return
    if args[1] == 'share':
        host = server.Server(working_dir=cwd)
        host.run()


main()
