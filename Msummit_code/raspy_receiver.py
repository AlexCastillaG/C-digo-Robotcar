##########Imports##########
import time
import comm_module
import pigpio
import RPi.GPIO as GPIO
import socket
import logging
import traceback


class RC_car():
    def __init__(self,PORT,servo_pin,esc_pin):
        self.PORT = PORT
        self.servo_pin = servo_pin
        self.esc_pin = esc_pin
        logging.basicConfig(filename='msummit.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.logger=logging.getLogger(__name__)            
        GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
        GPIO.setwarnings(False) #Disable warnings
        self.pi = pigpio.pi() # Connect to local Pi.
        while True:
                    
            try:
                self.receiver = comm_module.tcp_request("192.168.8.103",self.PORT,1024)
                break
            except ConnectionResetError:
                print("El mando ha sido desconectado", traceback.format_exc())
                continue
            except ConnectionRefusedError:
                print("El servidor esta offline, intentando reconectar", traceback.format_exc())
                continue
            except OSError:
                print("El dispositivo no esta conectado a internet", traceback.format_exc())
                continue
            except Exception:
                print("Unknown error: ", traceback.format_exc())
                raise


    def get_pwm(self,angle):
        return (angle/90) + 1500

    def log_err(self,error):
        self.logger.error(err)
        print(error)
        
    def log_info(self,info):
        self.logger.info(info)
        print(info)
        
    def angle_to_percent(self,angle):
        if angle > 180 or angle < 0:
            return False

        start = 800
        end = 2200
        ratio = (end - start)/180  # Calcul ratio from angle to percent

        angle_as_percent = angle * ratio

        return start + angle_as_percent
    
    def stop(self):
        data=[90,1500]
        self.pi.set_servo_pulsewidth(self.servo_pin , self.angle_to_percent(float(data[0])))
        self.pi.set_servo_pulsewidth(self.esc_pin,float(data[1]))     
        print("Se activo la parada de emergencia")
        
    def initialization(self):
  
        self.pi.set_servo_pulsewidth(self.servo_pin , 1500)
    
        self.pi.set_servo_pulsewidth(self.esc_pin, 0)

        self.pi.set_PWM_frequency(self.esc_pin,100)

        self.pi.set_servo_pulsewidth(self.esc_pin,2000)

        self.pi.set_servo_pulsewidth(self.esc_pin,1000)

        self.pi.set_servo_pulsewidth(self.esc_pin,1500)

    def start(self):

        while True:
            try:
                
                #self.logger.info(data)
                data = self.receiver.request()
                self.pi.set_servo_pulsewidth(self.servo_pin , self.angle_to_percent(float(data[1])))
                self.pi.set_servo_pulsewidth(self.esc_pin,float(data[0]))
            except ConnectionResetError:
                self.stop()
                self.receiver.s.close()
                print("El mando ha sido desconectado", traceback.format_exc())
            except ConnectionRefusedError:
                self.stop()
                self.receiver.s.close()
                print("El servidor esta offline, intentando reconectar", traceback.format_exc())
            except OSError:
                self.stop()
                self.receiver.s.close()
                print("El dispositivo no esta conectado a internet", traceback.format_exc())
            except ValueError:
                self.stop()
                self.receiver.s.close()
                print("Los datos recibidos no fueron los que se esperaban", traceback.format_exc())
            except Exception:
                self.stop()
                self.receiver.s.close()
                print("Unknown error: ", traceback.format_exc())

                

if __name__ == "__main__":
    summit = RC_car(5009,13,18)
    summit.initialization()
    summit.stop()
    summit.start()