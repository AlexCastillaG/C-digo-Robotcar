##########Imports##########
import time
import comm_module
import pigpio
import RPi.GPIO as GPIO
import socket
import logging 

class RC_car():
    def __init__(self,PORT,servo_pin,esc_pin):
        self.PORT = PORT
        self.servo_pin = servo_pin
        self.esc_pin = esc_pin
        self.receiver = comm_module.receiver_raspy("",self.PORT,1024)
        GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
        GPIO.setwarnings(False) #Disable warnings
        self.pi = pigpio.pi() # Connect to local Pi.
        self.logger = None

    def get_pwm(self,angle):
        return (angle/90) + 1500


    def angle_to_percent(self,angle):
        if angle > 180 or angle < 0:
            return False

        start = 800
        end = 2200
        ratio = (end - start)/180  # Calcul ratio from angle to percent

        angle_as_percent = angle * ratio

        return start + angle_as_percent
    
    def save_log(self, name):

        logging.basicConfig(filename="{}.log".format(name), format='%(asctime)s %(message)s', filemode='w') 
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        pass

    def initialization(self):
  
        self.pi.set_servo_pulsewidth(self.servo_pin , 1500)
    
        self.pi.set_servo_pulsewidth(self.esc_pin, 0)

        self.pi.set_PWM_frequency(self.esc_pin,100)

        self.pi.set_servo_pulsewidth(self.esc_pin,2000)

        self.pi.set_servo_pulsewidth(self.esc_pin,1000)

        self.pi.set_servo_pulsewidth(self.esc_pin,1500)

    def start(self):
        self.initialization()
        #self.save_log("logger")

        while True:
            try:
                data = self.receiver.receive()
                #self.logger.info(data)
                self.pi.set_servo_pulsewidth(self.servo_pin , self.angle_to_percent(float(data[1])))
                self.pi.set_servo_pulsewidth(self.esc_pin,float(data[0]))
            except ConnectionResetError:
                print("El mando ha sido desconectado")
                data=[90,1500]
                self.pi.set_servo_pulsewidth(self.servo_pin , self.angle_to_percent(float(data[0])))
                self.pi.set_servo_pulsewidth(self.esc_pin,float(data[1]))
            except Exception as e:
                data=[90,1500]
                self.pi.set_servo_pulsewidth(self.servo_pin , self.angle_to_percent(float(data[0])))
                self.pi.set_servo_pulsewidth(self.esc_pin,float(data[1]))   
                print("Unknown error: ",e)
                continue

                

if __name__ == "__main__":
    summit = RC_car(5009,13,18)
    summit.start()