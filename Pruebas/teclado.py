


from pyPS4Controller.controller import Controller
import pygame
import pprint
import os
import socket
import json
import time

#####################WIFICONF#######################
UDP_IP = "192.168.0.119"
UDP_PORT = 5005

#globalvars
velocity = 512; #max velocity
turn_angle = 90; #max turn angle
cal_angle = 90;
# DEFS


def get_speed(input_wheel): 

    vel_left=512
    vel_rigth=512
    total_vel=1024
    if (velocity>=512):
        if(input_wheel>=0):
            vel_rigth = velocity-total_vel*input_wheel/2
            vel_left = velocity
        if(input_wheel<0):  
            vel_rigth = velocity
            vel_left = velocity+total_vel*input_wheel/2
    if (velocity<512):
        if(input_wheel>=0):
            vel_rigth = velocity
            vel_left = velocity+total_vel*input_wheel/2
        if(input_wheel<0):  
            vel_rigth = velocity-total_vel*input_wheel/2
            vel_left = velocity


    return [int(vel_left),int(vel_rigth)]










def send(speed): #send the information to a client

    
    speed_l=str(int(speed[0])).zfill(4)
    speed_r=str(int(speed[1])).zfill(4)
    MESSAGE = bytes(str(speed_l+","+speed_r), encoding = "utf-8")

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: -1.0, 4: -1.0}#initilizate the axis you will use in this dictionary
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
            self.axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: -1.0}#initilizate the axis you will use in this dictionary

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
                        self.axis_data[event.axis] = round(event.value, 2)
                    elif event.type == pygame.JOYBUTTONUP:
                        self.button_data[event.button] = not self.button_data[event.button]
                        if event.button == 2:
                            while True:
                                time.sleep(0.1)
                                send([512, 512])
                        global velocity
                        if event.button == 0 and velocity<=998:
                            velocity=velocity+30
                        if event.button == 1 and velocity>=30:
                            velocity=velocity-30
                        else:
                            if event.button == 4:
                                self.button_data.update({5: False})
                            elif event.button == 5:
                                self.button_data.update({4: False})
                            #pprint.pprint("4: {}".format(self.button_data.get(4)))
                            #pprint.pprint("5: {}".format(self.button_data.get(5)))
                    elif event.type == pygame.JOYHATMOTION:
                        self.hat_data[event.hat] = event.value

                    # Insert your code on what you would like to happen for each event here!
                    # In the current setup, I have the state simply printing out to the screen.


                    #pprint.pprint(get_speed(self.axis_data.get(
                    #     4),self.axis_data.get(3) ,self.button_data.get(5),self.button_data.get(4)))
                    # pprint.pprint(self.button_data.get(5))
                    #pprint.pprint(self.axis_data.get(0))
                    current_speed = get_speed(self.axis_data.get(0))                  
                    time.sleep(0.01)
                    pprint.pprint("Speed: "+str(current_speed))
                    send(current_speed)
                
if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
