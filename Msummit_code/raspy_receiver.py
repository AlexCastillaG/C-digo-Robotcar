##########Imports##########
import time
import comm_module
import pigpio
import RPi.GPIO as GPIO
import socket


class RC_car():
    def __init__(self,PORT,servo_pin,esc_pin):
        self.PORT = PORT
        self.servo_pin = servo_pin
        self.esc_pin = esc_pin
        self.receiver = comm_module.receiver_raspy("",self.PORT,1024)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.servo_pin, 50)  
          



    def initialization(self):

        self.servo.start(2.5)  
        
        #self.pi.set_servo_pulsewidth(self.esc_pin , 0)

        #self.pi.set_PWM_frequency(self.esc_pin ,100)

        #self.pi.set_servo_pulsewidth(self.esc_pin ,2000)

        #self.pi.set_servo_pulsewidth(self.esc_pin ,1000)

        #self.pi.set_servo_pulsewidth(self.esc_pin ,1500)

    def start(self):
        self.initialization()

        while True:
            data = self.receiver.receive()
            print("speed: %s"% data[0]," angle: %s",data[1])
            self.servo.ChangeDutyCycle(int(data[1]))
            #self.pi.set_servo_pulsewidth(self.esc_pin ,data[0])

if __name__ == "__main__":
    summit = RC_car(5009,13,18)
    summit.start()