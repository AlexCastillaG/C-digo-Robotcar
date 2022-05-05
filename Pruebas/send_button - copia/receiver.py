import socket
import sys
from read_ip_from_file import get_ip_and_port

BUFFER_SIZE=1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5051))
server.listen(1)

def get_datos():
    cli, addr =server.accept()
    check = cli.recv(1024)
    cli.close()
    return check

while True:
    print(get_datos())