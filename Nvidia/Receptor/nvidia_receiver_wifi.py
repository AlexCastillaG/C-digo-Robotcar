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
kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range[1000,2000]


#defs


def initialization():

    kit.servo[0].angle=0
    kit.servo[0].angle=180
    kit.servo[0].angle=0
    kit.servo[0].angle=90


#main

initialization()

while True:
    data, addr = sock.recvfrom(1024)
    message= json.loads(data.decode())
    print("speed: %s"% message.get("speed")+" angle: %s"% message.get("angle"))
    kit.servo[0].angle=message.get("speed")
    ###############



