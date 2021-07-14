from pyPS4Controller.controller import Controller
import pygame
import pprint
import os,sys
import socket
import json
import time

#####################WIFICONF#######################
TCP_IP = "192.168.2.130"
TCP_PORT = 5005
BUFFER_SIZE = 1024


# globalvars
velocidad = 5  # max velocidad
turn_angle = 90  # max turn angle
cal_angle = 90
# DEFS


# get speed adapted to pwm signal with the pedal inputs
def get_speed(input_fpedal, input_brake):
    # booleans select the direcction
    brake = (input_brake+1)/2
    speed = (input_fpedal+1)/2

    speed = 90+velocidad*speed-velocidad*brake


    return speed





# get the angle adapted to pwm signal depending on the wheel input
def get_angle_pwm(input_wheel):

    angle = 90

    if input_wheel < 0:
        input_wheel = -input_wheel
        angle = cal_angle-turn_angle*input_wheel
    elif input_wheel >= 0:
        angle = cal_angle+turn_angle*input_wheel

    return angle


def send(speed, angle):  # send the information to a client

    data = json.dumps({"speed": speed, "angle": angle})
    MESSAGE = data.encode("utf-8")

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    sock.connect((TCP_IP,TCP_PORT))
    sock.send(MESSAGE)
    data = sock.recv(BUFFER_SIZE)
    sock.close()


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    # initilizate the axis you will use in this dictionary
    axis_data={0: 0.0, 1: 0.0, 2: 0.0, 3: -1.0, 4: -1.0}
    button_data = {}
    deadman=False
                                            
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
                    if event.button == 4:
                        self.deadman=False
                        print("Por seguridad se ha activado el protocolo de parada automática"+"\n"+"Pulse el deadman para volver a tomar el control")
                    self.button_data[event.button] = not self.button_data[event.button]
                    global velocidad
                    if event.button == 0:
                        if velocidad >= 90:
                            break
                        else:
                            velocidad = velocidad+5
                    if event.button == 1:
                        if velocidad <= 0:
                            break
                        else:
                            velocidad = velocidad-5
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 4:
                        self.deadman=True
                        


                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.

                # pprint.pprint(self.axis_data.get(4))
                # pprint.pprint(get_speed(self.axis_data.get(
                #     4),self.axis_data.get(3) ,self.button_data.get(5),self.button_data.get(4)))
                # pprint.pprint(self.button_data.get(5))
                #pprint.pprint(self.button_data)
                
                joystick_acelerador=self.axis_data.get(4)
                joystick_freno=self.axis_data.get(3)
                joystick_volante=self.axis_data.get(0)

                
                current_speed = get_speed(joystick_acelerador, joystick_freno)
                current_pwm_angle = get_angle_pwm(joystick_volante)
                time.sleep(0.01)
                if self.deadman:  
                    pprint.pprint("Speed: "+str(current_speed) +
                             " Angle: "+str(current_pwm_angle))
                    send(current_speed, current_pwm_angle)
                else:
                    send(90, 90) 

                    

if __name__ == "__main__":
    
    try:
        ps4 = PS4Controller()
        ps4.init()
        ps4.listen()
    except:
        print("No se pudo iniciar el programa",sys.exc_info()[0])
        raise