import pygame
import comm_module
import time
import os
import threading
class PS4Controller():


    def __init__(self,usb_port,deadman_port,speedup_port,speeddown_port,throttle_port_input,brake_port_input,wheel_port_input):

        pygame.init()
        pygame.joystick.init()

        self.controller = pygame.joystick.Joystick(usb_port)

        self.controller.init()
        self.axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0} #Value of all the controller's axis
        self.button_data = self.map_buttons() #Value all the controller's buttons
        self.deadman = False #Deadman will force the user to push a button if he/she want to move
        self.max_speed = 5 #Set the max car speed
        self.max_turn_angle = 90 #Set the max car turn angle 
        self.current_speed = 0 #Storage the current car speed
        self.current_angle = 0 #Storage the current car speed
        self.cal_angle = 90 #This var is used to set which angle is fuly forward
        self.cal_speed = 77 #This var is used to set the neutral position of the throttle 
        self.throttle_port = throttle_port_input
        self.brake_port = brake_port_input
        self.wheel_port = wheel_port_input
        self.joystick_throttle=self.axis_data.get(self.throttle_port) #Select what axis will act as throttle
        self.joystick_brake=self.axis_data.get(self.brake_port) #Select what axis will act as brake
        self.joystick_wheel=self.axis_data.get(self.wheel_port) #Select what axis will act as wheel
        self.deadman_button = deadman_port #Select what button will act as deadman
        self.speedup_button = speedup_port #Select what button will act as speedup
        self.speeddown_button = speeddown_port #Select what button will act as speeddown
        self.control_sender = comm_module.sender("control_netinfo.txt")
        self.GUI_sender = comm_module.sender("GUI_netinfo.txt")

    def get_params(self):
        #print(self.current_speed,self.current_angle,self.deadman,self.max_speed)
        return self.current_speed,self.current_angle,self.deadman,self.max_speed

    def map_buttons(self):
        button_data = {}
        for i in range(self.controller.get_numbuttons()):
            button_data[i] = False
        return button_data

    def get_speed(self,input_fpedal, input_brake):
        brake = (input_brake+1)/2
        #print(input_brake)
        speed = (input_fpedal+1)/2
        #print(input_fpedal)

        speed = self.cal_speed+self.max_speed*speed-self.max_speed*brake
        if speed<0:
            speed=0

        return round(speed,2)

    def get_angle_pwm(self,input_wheel):
        #print(input_wheel)
        if input_wheel < 0:
            input_wheel = -input_wheel
            angle = self.cal_angle-self.max_turn_angle*input_wheel
        elif input_wheel >= 0:
            angle = self.cal_angle+self.max_turn_angle*input_wheel

        return round(angle,2)


    def mapping_tool(self):
        self.listen()
        os.system("cls")
        print(" Axis: ","\n",self.axis_data,"\n","Buttons: ","\n",self.button_data)
        

    def listen(self):

        for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == self.deadman_button:
                        self.deadman=False
                        print("Por seguridad se ha activado el protocolo de parada automática"+"\n"+"Debes mantener pulsado el deadman mientras conduce")
                    self.button_data[event.button] = not self.button_data[event.button]
                    if event.button == self.speedup_button:
                        if self.max_speed >= 90:
                            break
                        else:
                            self.max_speed = self.max_speed+5
                    if event.button == self.speeddown_button:
                        if self.max_speed <= 0:
                            break
                        else:
                            self.max_speed = self.max_speed-5
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == self.deadman_button:
                        self.deadman=True
                        
        self.joystick_throttle=self.axis_data.get(self.throttle_port) #Select what axis will act as throttle
        self.joystick_brake=self.axis_data.get(self.brake_port) #Select what axis will act as brake
        self.joystick_wheel=self.axis_data.get(self.wheel_port) #Select what axis will act as wheel
        self.current_speed = self.get_speed(self.joystick_throttle, self.joystick_brake)
        self.current_angle = self.get_angle_pwm(self.joystick_wheel)

    def GUI_send(self):
        while True:
            self.GUI_sender.send("GUI",self.current_speed,self.current_angle,self.deadman,self.max_speed)

    def move_car(self):
        while True:
            self.listen()
            if self.deadman:
                self.control_sender.send("Car",self.current_speed,self.current_angle)
            else:
                self.control_sender.send("Car",77.00,90.00)
                #print(speed,angle)
                #print(self.joystick_wheel)
    def dual_send(self):
        GUI=threading.Thread(target=self.GUI_send)
        GUI.start()

        car=threading.Thread(target=self.move_car)
        car.start()

        car.join()
        GUI.join()    