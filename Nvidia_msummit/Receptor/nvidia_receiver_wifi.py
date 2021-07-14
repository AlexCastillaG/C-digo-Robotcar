##########Imports##########
import time
import os
import sys, tty, termios
import RPi.GPIO as GPIO
import socket,json


##########WIFICONF##########
########## TCP ##########
TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#connections, vars and pins



#defs

def receive():
    conn, addr = s.accept()
    data= conn.recv(BUFFER_SIZE)
    conn.close()

    message= json.loads(data.decode("utf-8"))  
    
    return message

def initialization():

    kit.servo[0].angle=0
    kit.servo[0].angle=180
    kit.servo[0].angle=0
    kit.servo[0].angle=90



def __init__(s):
    
    initialization()

    while True:
        
        message = receive()
        print("speed: %s"% message.get("speed")+" angle: %s"% message.get("angle"))
        kit.servo[0].angle=message.get("speed")
        time.sleep(0.01)

#main
__init__(s)