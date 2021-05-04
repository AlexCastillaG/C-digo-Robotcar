##########Imports##########
import time
import os
import sys, tty, termios
import pigpio
import RPi.GPIO as GPIO
import socket,json


##########WIFICONF##########
UDP_IP= ""
UDP_PORT= 5005
sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#connections, vars and pins
ESC = 13
GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings
Servo = 18
frequence = 50
pi = pigpio.pi() # Connect to local Pi.

#defs
def angle_to_pwm(angle):
    if angle > 180 or angle < 0:
        return False

    start = 1000
    end = 2000
    ratio = (end - start)/180  # Calcul ratio from angle to percent

    angle_as_pwm = angle * ratio

    return start + angle_as_pwm

def initialization():

    
    pi.set_servo_pulsewidth(ESC, 0)

    pi.set_PWM_frequency(ESC,100)

    pi.set_servo_pulsewidth(ESC,2000)

    pi.set_servo_pulsewidth(ESC,1000)

    pi.set_servo_pulsewidth(ESC,1500)


#main

initialization()

while True:
    data, addr = sock.recvfrom(1024)
    message= json.loads(data.decode())
    print("speed: %s"% message.get("speed")+" angle: %s"% message.get("angle"))
    pi.set_servo_pulsewidth(Servo , angle_to_pwm(message.get("angle")))
    pi.set_servo_pulsewidth(ESC,message.get("speed"))


