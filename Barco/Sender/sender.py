from pyPS4Controller.controller import Controller
import pygame
import pprint
import os
import socket
import json
import time
import threading


#####################WIFICONF#######################
UDP_IP = "192.168.0.107"
UDP_PORT = 5005

#globalvars
cal_angle = 90;

# DEFS

class ThreadClass(threading.Thread):
    
  def run(self):
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()

def send(speed, angle): #send the information to a client

    data = json.dumps("$ZR,"+str(angle)+","+str(speed)+"\n\r" )
    #pprint.pprint("$ZR,"+str(angle)+","+str(speed)+"\n\r" )
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

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(1)
        self.controller.init()
        pprint.pprint(pygame.joystick.get_count)



    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {0: 0.0}#initilizate the axis you will use in this dictionary

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
                            send(1500,90)
                            exit()
                        global velocity
                        if event.button == 0:
                            if velocity >= 500:
                                velocity=450
                            velocity=velocity+10
                        if event.button == 1:
                            velocity=velocity-10
                            if velocity <= 0:
                                velocity=50
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

                    pprint.pprint(self.axis_data)
                    #pprint.pprint(get_speed(self.axis_data.get(
                    #     4),self.axis_data.get(3) ,self.button_data.get(5),self.button_data.get(4)))
                    # pprint.pprint(self.button_data.get(5))
                    #pprint.pprint(self.button_data)
                    current_speed = int(self.axis_data.get(0)*100)
                    current_pwm_angle = int(self.axis_data.get(0)*100)
                   # pprint.pprint("Speed: "+str(current_speed)+ " Angle: "+str(current_pwm_angle))
                    send(current_speed,current_pwm_angle)



if __name__ == "__main__":

    PS4 = ThreadClass()
    PS4.start()

    