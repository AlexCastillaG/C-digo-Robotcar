import socket
import sys
from read_ip_from_file import get_ip_and_port

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port

ip,port,check = get_ip_and_port()
server_address = ip, port
sock.bind(server_address)
sock.listen(1)

while True:

    connection, client_address = sock.accept()
    try:

        while True:

            if check:
                data = connection.recv(16)
                print(data)
                if data:
                    connection.sendall(data)
                else:
                    print('no data from', client_address)
                    break

    finally:
        connection.close()