import socket
import sys
from read_ip_from_file import get_ip_and_port
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip,port,check = get_ip_and_port()
server_address = ip, port
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
i=0
try:

    while True:
        if check:
            sleep(0.5)
            i = i+1
            
            message = str(i).encode("utf-8")
            sock.sendall(message)     
            data = sock.recv(16)

finally:
    print('closing socket')
    sock.close()