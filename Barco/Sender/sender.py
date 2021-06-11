from pyPS4Controller.controller import Controller
import pygame
import pprint
import os
import socket
import json
import time
import threading


#####################WIFICONF#######################
UDP_IP = "192.168.0.194"
UDP_PORT = 5005

#globalvars
cal_angle = 90;
turn_angle = 90;
# DEFS
 


def angle_to_pwm(angle):
    if angle > 180 or angle < 0:
        return False

    start = 1000
    end = 2000
    ratio = (end - start)/180  # Calcul ratio from angle to percent

    angle_as_pwm = angle * ratio

    return start + angle_as_pwm

def get_angle_pwm(input_wheel):#get the angle adapted to pwm signal depending on the wheel input

    angle = 90

    if input_wheel < 0:
        input_wheel = -input_wheel
        angle = cal_angle-turn_angle*input_wheel
    elif input_wheel >= 0:
        angle = cal_angle+turn_angle*input_wheel

    pwm_signal = angle_to_pwm(angle)

    return pwm_signal
class ThreadClass_PS4(threading.Thread):
    
  def run(self):
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()

class ThreadClass_Throttle(threading.Thread):
    
  def run(self):
    throttle = throttleController()
    throttle.init()
    throttle.listen()

def send(speed, angle): #send the information to a client

    data = json.dumps({"speed": speed, "angle": angle})
    MESSAGE = data.encode()

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    
    controller = None
    axis_data = {0: 0.0,}#initilizate the axis you will use in this dictionary
    button_data = None
    hat_data = None
    contador=0
    
    
    def init(PS4Controller):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        PS4Controller.controller = pygame.joystick.Joystick(1)
        PS4Controller.controller.init()
        pprint.pprint(pygame.joystick.get_count)



    def listen(PS4Controller):
        """Listen for events to happen"""

        if not PS4Controller.axis_data:
            PS4Controller.axis_data = {0: 0.0}#initilizate the axis you will use in this dictionary

        if not PS4Controller.button_data:
            PS4Controller.button_data = {}
            for i in range(PS4Controller.controller.get_numbuttons()):
                PS4Controller.button_data[i] = False


        while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        PS4Controller.axis_data[event.axis] = round(event.value, 2)
                    elif event.type == pygame.JOYBUTTONUP:
                        PS4Controller.button_data[event.button] = not PS4Controller.button_data[event.button]
                        if event.button == 2:
                            send(1500,1500)
                            exit()
                        


                    # Insert your code on what you would like to happen for each event here!
                    # In the current setup, I have the state simply printing out to the screen.
                
                    PS4Controller.contador=PS4Controller.contador+10
                    print(PS4Controller.contador)
                   # pprint.pprint(self.axis_data.get(1))
                    #pprint.pprint(get_speed(self.axis_data.get(
                    #     4),self.axis_data.get(3) ,self.button_data.get(5),self.button_data.get(4)))
                    # pprint.pprint(self.button_data.get(5))
                    #pprint.pprint(self.button_data)
                   # current_speed = int(get_angle_pwm(self.axis_data.get(1)))
                    current_pwm_angle = int(get_angle_pwm(PS4Controller.axis_data.get(0)))
                    #print("angle:" + str(current_pwm_angle))
                   # pprint.pprint("Speed: "+str(current_speed)+ " Angle: "+str(current_pwm_angle))
                   # send(current_speed,current_pwm_angle)

class throttleController(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    contador=0
    controller = None
    axis_data_2 = {0: 0.0,}#initilizate the axis you will use in this dictionary
    button_data = None
    hat_data = None

    def init(throttleController):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        throttleController.controller = pygame.joystick.Joystick(0)
        throttleController.controller.init()
        pprint.pprint(pygame.joystick.get_count)



    def listen(throttleController):
        """Listen for events to happen"""

        if not throttleController.axis_data_2:
            throttleController.axis_data_2 = {0: 0.0}#initilizate the axis you will use in this dictionary


        while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        throttleController.axis_data_2[event.axis] = round(event.value, 2)

                    # Insert your code on what you would like to happen for each event here!
                    # In the current setup, I have the state simply printing out to the screen.

                    #pprint.pprint(self.axis_data_2)

                    current_pwm_angle = int(get_angle_pwm(throttleController.axis_data_2.get(0)))
                    #print("speed: " + str(current_pwm_angle))

                
                throttleController.contador=throttleController.contador+50
               # print("____"+str(throttleController.contador))

if __name__ == "__main__":

    hilo_ps4=ThreadClass_PS4()
    hilo_ps4.start()
    hilo_Throttle=ThreadClass_Throttle()
    hilo_Throttle.start()
