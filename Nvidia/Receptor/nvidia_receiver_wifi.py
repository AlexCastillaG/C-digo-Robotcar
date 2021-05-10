##########Imports##########
import time
import os
import sys, tty, termios
import RPi.GPIO as GPIO
import socket,json


##########WIFICONF##########
UDP_IP= ""
UDP_PORT= 5005
sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#connections, vars and pins




#defs


#def initialization():




#main

#initialization()

while True:
    data, addr = sock.recvfrom(1024)
    message= json.loads(data.decode())
    print("speed: %s"% message.get("speed")+" angle: %s"% message.get("angle"))
    ###############



