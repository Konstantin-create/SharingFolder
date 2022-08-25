import socket
import requests


def is_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
