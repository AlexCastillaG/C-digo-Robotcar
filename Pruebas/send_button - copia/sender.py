import socket
import sys
from read_ip_from_file import get_ip_and_port
from time import sleep

import socket




BUFFER_SIZE=1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5050))
server.listen(1)

def get_data_check():
    cli, addr =server.accept()
    check = cli.recv(1024)
    cli.close()
    return check

def sendcar(number):
  
    sock = socket.socket(socket.AF_INET,  # Internet
                                socket.SOCK_STREAM)  # TCP
    sock.connect(("localhost",5051))
    sock.send(number)
    data = sock.recv(1024)
    sock.close()



i=0
while True:
    i=i+1
    if get_data_check().decode("utf-8") == "True":
        flag = True
    elif get_data_check().decode("utf-8")  == "False":
        flag = False
    if flag:
        sendcar(str(i).encode("utf-8"))



