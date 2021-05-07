from pyPS4Controller.controller import Controller
import pygame
import pprint
import os
import socket
import json
import time

#####################WIFICONF#######################
UDP_IP = "192.168.0.194"
UDP_PORT = 5005

#globalvars
velocity = 50; #max velocity
turn_angle = 90; #max turn angle
cal_angle = 90;
# DEFS
def angle_to_pwm(angle):
    if angle > 180 or angle < 0:
        return False

    start = 1000
    end = 2000
    ratio = (end - start)/180  # Calcul ratio from angle to percent

    angle_as_pwm = angle * ratio

    return start + angle_as_pwm

def get_speed(input_fpedal, input_brake, forward, backward): #get speed adapted to pwm signal with the pedal inputs
#booleans select the direcction
    brake = (input_brake+1)/2
    speed = (input_fpedal+1)/2
    if forward:
        speed = 1500+velocity*speed-velocity*brake
        if speed<1500:
            speed=1500
    elif backward:
        speed = 1500-velocity*speed+velocity*brake
        if speed>1500:
            speed=1500
    else:
        speed = 1500
    return speed


def get_angle_pwm(input_wheel):#get the angle adapted to pwm signal depending on the wheel input

    angle = 90

    if input_wheel < 0:
        input_wheel = -input_wheel
        angle = cal_angle-turn_angle*input_wheel
    elif input_wheel >= 0:
        angle = cal_angle+turn_angle*input_wheel

    pwm_signal = angle_to_pwm(angle)

    return pwm_signal



def send(speed, angle): #send the information to a client

    data = json.dumps({"speed": speed, "angle": angle})
    MESSAGE = data.encode()

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

                    #pprint.pprint(self.axis_data.get(4))
                    #pprint.pprint(get_speed(self.axis_data.get(
                    #     4),self.axis_data.get(3) ,self.button_data.get(5),self.button_data.get(4)))
                    # pprint.pprint(self.button_data.get(5))
                    #pprint.pprint(self.button_data)
                    current_speed = get_speed(self.axis_data.get(4),self.axis_data.get(3),self.button_data.get(5),self.button_data.get(4))
                    current_pwm_angle = get_angle_pwm(self.axis_data.get(0))
                    pprint.pprint("Speed: "+str(current_speed)+ " Angle: "+str(current_pwm_angle))
                    send(current_speed,current_pwm_angle)

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
