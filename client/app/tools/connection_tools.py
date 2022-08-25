import socket
import requests


def is_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def check_ip(ip):
    if not is_ip(ip):
        return False
    try:
        requests.get(f'http://{ip}:8888', timeout=5)
        return True
    except:
        return False
