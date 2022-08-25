import socket


def is_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


print(is_ip('129.23.212.2'))
