import json
import socket


def is_ip(ip: str) -> bool:
    """Function to check is string ip"""

    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
