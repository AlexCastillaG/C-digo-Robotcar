from pyPS4Controller.controller import Controller
import pygame
import pprint
import os,sys
import socket
import json
import time
from get_ip import get_ip_and_port

#####################WIFICONF#######################

TCP_IP,TCP_PORT,check = get_ip_and_port()
BUFFER_SIZE = 1024
interfazPort=5050


# DEFS


# get speed adapted to pwm signal with the pedal inputs
def get_speed(input_fpedal, input_brake):
    # booleans select the direcction
    brake = (input_brake+1)/2
    #print(input_brake)
    speed = (input_fpedal+1)/2
    #print(input_fpedal)

    speed = 77+velocidad*speed-velocidad*brake
    if speed<0:
        speed=0

    return speed





# get the angle adapted to pwm signal depending on the wheel input



def send(speed, angle):  # send the information to a client

    data = json.dumps({"speed": round(speed,2), "angle": round(angle,2)})
    message = data.encode("utf-8")

    sock = socket.socket(socket.AF_INET,  
                         socket.SOCK_STREAM)  
    sock.connect((TCP_IP,TCP_PORT))
    sock.send(message)
    data = sock.recv(BUFFER_SIZE)
    sock.close()
    #print(data)



        



class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data={0: 0.0, 1: 1.0, 2: 1.0, 3: 0.0, 4: 0.0}
    button_data = {}
    deadman=False
    speed = 77.00
    angle = 90.00
    velocidad = 5 
    turn_angle = 90 


    def get_turn_angle():
        return PS4Controller.turn_angle

    def get_GUI_data(speed, angle, deadman, maxSpeed):
    
        return speed, angle, deadman, maxSpeed   

    def get_angle_pwm(input_wheel):

        angle = 90

        if input_wheel < 0:
            input_wheel = -input_wheel
            angle = PS4Controller.get_turn_angle()-PS4Controller.get_turn_angle()*input_wheel
        elif input_wheel >= 0:
            angle = PS4Controller.get_turn_angle()+PS4Controller.get_turn_angle()*input_wheel

        return angle


    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False


        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 1:
                        self.deadman=False
                        print("Por seguridad se ha activado el protocolo de parada automática"+"\n"+"Debes mantener pulsado el deadman mientras conduce")
                    self.button_data[event.button] = not self.button_data[event.button]
                    global velocidad
                    if event.button == 3:
                        if velocidad >= 90:
                            break
                        else:
                            velocidad = velocidad+5
                    if event.button == 5:
                        if velocidad <= 0:
                            break
                        else:
                            velocidad = velocidad-5
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1:
                        self.deadman=True
            #print(self.axis_data)            
                
            joystick_acelerador=self.axis_data.get(1)
            joystick_freno=self.axis_data.get(2)
            joystick_volante=self.axis_data.get(0)               
            current_speed = get_speed(joystick_acelerador, joystick_freno)
            current_pwm_angle = self.get_angle_pwm(joystick_volante)
            time.sleep(0.01)
            #print(self.button_data)

            if self.deadman:  
                pprint.pprint("Speed: "+str(current_speed) +
                             " Angle: "+str(current_pwm_angle))
                try:
                    if check:
                        send(current_speed, current_pwm_angle)
                        self.get_GUI_data(current_speed, current_pwm_angle,False, velocidad)
                    #pprint.pprint("Speed: "+str(current_speed) +
                    #         " Angle: "+str(current_pwm_angle))

                except:
                    raise
                    print("El coche se ha desconectado, compruebe la conexión")
                    continue
            else:
                try:
                    if check:
                        send(77.00, 90.00) 
                    self.get_GUI_data(current_speed, current_pwm_angle,False, velocidad)
                except:
                    raise
                    print("El coche se ha desconectado, compruebe la conexión")
                    continue                    

                    

if __name__ == "__main__":
    

    
    try:
        ps4 = PS4Controller()
        ps4.init()
        ps4.listen()       
    except:
            print("No se pudo iniciar el programa",sys.exc_info()[0])
            raise