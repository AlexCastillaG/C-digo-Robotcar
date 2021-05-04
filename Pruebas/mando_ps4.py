import socket, json

#####################WIFICONF#######################
UDP_IP = "192.168.0.255"
UDP_PORT = 5005

#DEFS
def convert(x,y):
    angle=90
    speed=1500
    if x<0:
        x=-x
        angle=90-70*x
    elif x>=0:
        angle=90+70*x

    speed = 1500-100*y

    control = [angle, speed]
        

    return control
def send(angle,speed):

    control=convert(angle,speed)
    speed=control[1]
    angle=control[0]
    data = json.dumps({"speed": speed, "angle": angle})
    MESSAGE=data.encode()
  

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
from pyPS4Controller.controller import Controller


import os
import pprint
import pygame

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                
                pprint.pprint(self.axis_data)

               # send(self.axis_data.get(0),self.axis_data.get(3))


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()