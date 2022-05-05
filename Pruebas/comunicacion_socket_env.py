#!/usr/bin/env python

#Variables
#Se importa el módulo
import socket
import time
import pygame
from decimal import Decimal
#Creación de un objeto socket (lado cliente)
#Variables
host = 'localhost'
port = 8050
#Se importa el módulo
import socket
 
#Creación de un objeto socket (lado cliente)
obj = socket.socket()
 
#Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.connect((host, port))
print("Conectado al servidor")

def send(input_palanca): #send the information to a client



    mens = str(input_palanca)
    print(mens)
    #Con el método send, enviamos el mensaje
    obj.send(mens.encode("ascii"))




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
        self.controller = pygame.joystick.Joystick(1)
        self.controller.init()




    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {0: 0, 1: 0.0, 2: 0.0, 3: 0.0, 4: -1.0}#initilizate the axis you will use in this dictionary

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False



        while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value, 2)

        
                time.sleep(0.01)
                print(self.axis_data.get(0))
                send(self.axis_data.get(0))
if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
    #Cerramos la instancia del objeto servidor
    obj.close()
    print("Conexión cerrada")