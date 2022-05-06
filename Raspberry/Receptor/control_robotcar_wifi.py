##########Imports##########
import time
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


def initialization():

    
    pi.set_servo_pulsewidth(ESC, 0)

    pi.set_PWM_frequency(ESC,100)

    pi.set_servo_pulsewidth(ESC,2000)

    pi.set_servo_pulsewidth(ESC,1000)

    pi.set_servo_pulsewidth(ESC,1500)


#main

initialization()

while True:
    time.sleep(0.01)
    data, addr = sock.recvfrom(1024)
    message= json.loads(data.decode())
    print("speed: %s"% message.get("speed")+" angle: %s"% message.get("angle"))
    pi.set_servo_pulsewidth(Servo , (message.get("angle")))
    pi.set_servo_pulsewidth(ESC,message.get("speed"))


