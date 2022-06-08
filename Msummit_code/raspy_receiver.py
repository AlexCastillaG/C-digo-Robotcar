##########Imports##########
import time
import comm_module
import pigpio
import RPi.GPIO as GPIO
import socket
import logging
import traceback


class RC_car():
    def __init__(self,servo_pin,esc_pin):
        self.servo_pin = servo_pin
        self.esc_pin = esc_pin
        
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename= 'msummit.txt',
                            filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger().addHandler(console)
        
        GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
        GPIO.setwarnings(False) #Disable warnings
        self.pi = pigpio.pi() # Connect to local Pi.
        
        
    def create_receiver(self):
        self.receiver = comm_module.tcp_request(1024)


    def get_pwm(self,angle):
        return (angle/90) + 1500

    def log_info(self,info):
        logging.info(info)
        
    def close_connection(self):
        self.receiver.close_connection()
        
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
        self.log_info("Se activo la parada de emergencia")
        
    def initialization(self):
  
        self.pi.set_servo_pulsewidth(self.servo_pin , 1500)
    
        self.pi.set_servo_pulsewidth(self.esc_pin, 0)

        self.pi.set_PWM_frequency(self.esc_pin,100)

        self.pi.set_servo_pulsewidth(self.esc_pin,2000)

        self.pi.set_servo_pulsewidth(self.esc_pin,1000)

        self.pi.set_servo_pulsewidth(self.esc_pin,1500)

    def move(self):
   
        data = self.receiver.request()
        self.log_info(data)
        self.pi.set_servo_pulsewidth(self.servo_pin , self.angle_to_percent(float(data[1])))
        self.pi.set_servo_pulsewidth(self.esc_pin,float(data[0]))
        
    def run_exception_protocol(self, info):
        self.stop()
        self.try_connection()
        self.log_info(info)

    def try_connection(self):
        while True:
            try:
                summit.create_receiver()
                break
                self.log_info("El host rechazo la conexion, reintentado...")
                continue            
            except socket.timeout:
                self.log_info("El dispositivo no se pudo conectar, reintentado...")
                continue
            except OSError:
                self.log_info("El dispositivo no se pudo conectar, reintentado...")
                continue  

if __name__ == "__main__":
    

    SERVO_PIN=13
    ESC_PIN=18
    summit = RC_car(SERVO_PIN,ESC_PIN)
    summit.initialization()
    summit.try_connection()
    summit.stop()
    
    while True:
        try:
            summit.move()
        except ConnectionResetError:
            summit.run_exception_protocol(("El mando ha sido desconectado", traceback.format_exc()))
            
        except ConnectionRefusedError:
            summit.run_exception_protocol(("El servidor esta offline, intentando reconectar", traceback.format_exc()))
            
        except OSError:
            summit.run_exception_protocol(("El dispositivo no esta conectado a internet", traceback.format_exc()))

        except ValueError:
            summit.run_exception_protocol(("Los datos recibidos no fueron los que se esperaban", traceback.format_exc()))
            
        except Exception:
            summit.run_exception_protocol(("Unknown error: ", traceback.format_exc()))

