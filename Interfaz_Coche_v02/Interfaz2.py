#####################IMPORTS#######################
import socket
import os
import time
import threading
import time
import PySimpleGUI as sg
import pickle
import traceback
from PySimpleGUI.PySimpleGUI import Titlebar, Window
import json
from PIL import Image
#####################VARIABLES#######################
velocidad=0.0
angulo=0.0
deadman=False
velocidad_max=0.0
estado='Parado'
speed_images = ["images\\velocidad_PARADO.png","images\\velocidad_1.png","images\\velocidad_2.png","images\\velocidad_3.png",
"images\\velocidad_4.png","images\\velocidad_5.png","images\\velocidad_6.png","images\\velocidad_MAX.png"]

imgVelocidad = speed_images[0]
imgVolante = "images\\volante_original.png"
imgSemaforo = "images\semaforo_rojo.png"

ip="localhost"
Port=5007
BUFFER_SIZE=1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, Port))
server.listen(1)
#####################GUI#######################

layout = [[sg.Image("images\logoiteam.png",size=(512,170),background_color="white")],


[sg.Image("images\coche_rees.png",size=(512,304),background_color="white")],

[sg.Text("V: " + str(round(velocidad,2))+"Km/h " + '\n' + "VMax = " + '\n' + estado + str(velocidad_max)+" Km/h",text_color="black",key="velocidadInterfaz", background_color="white"), sg.Image(imgVelocidad,size=(152,147),key="imgVelInterfaz",background_color="white"), sg.Image(imgSemaforo,size=(110,110),key="imgSemaforo",background_color="white"), sg.Image(imgVolante,size=(217,217),key="imgVolante",background_color="white"),  sg.Text("          ",background_color="white")]

]
############################################

def get_datos():
    cli, addr =server.accept()
    data = cli.recv(1024)
    fiveg_data= json.loads(data.decode("utf-8"))
    cli.close()
    velocidad=fiveg_data.get("speed")
    angulo=fiveg_data.get("angle")
    deadman=fiveg_data.get("deadman")
    velocidad_max=fiveg_data.get("maxSpeed")
    #print(velocidad,angulo,deadman,velocidad_max)
    return velocidad, angulo, deadman, velocidad_max


def img_volante (angulo):

    angulo=int(angulo-90)
    im = Image.open('images\\volante_original.png')
    im=im.rotate(angulo)
    im.save('images\\volante.png')
    im.close()



def img_velocidad (velocidad, velocidad_max):
    
    velocidad_max = velocidad_max/7

    if velocidad==0:
        imgVelocidad = speed_images[0]

    elif velocidad>0 and velocidad <= velocidad_max:
        imgVelocidad = speed_images[1]

    elif velocidad>velocidad_max and velocidad <= 2*velocidad_max:
        imgVelocidad = speed_images[2]

    elif velocidad>2*velocidad_max and velocidad <= 3*velocidad_max:
        imgVelocidad = speed_images[3]

    elif velocidad>3*velocidad_max and velocidad <= 4*velocidad_max:
        imgVelocidad = speed_images[4]

    elif velocidad>4*velocidad_max and velocidad <= 5*velocidad_max:
        imgVelocidad = speed_images[5]

    elif velocidad>5*velocidad_max and velocidad <= 6*velocidad_max:
        imgVelocidad = speed_images[6]

    elif velocidad>6*velocidad_max:
        imgVelocidad = speed_images[7]

    else: 
        imgVelocidad = speed_images[0]    
    return imgVelocidad

def img_semaforo (deadman):
    if deadman == True:
        imgSemaforo = "images\semaforo_verde.png"

    else: 
        imgSemaforo = "images\semaforo_rojo.png"
    return imgSemaforo

#def angulo_ajuste (angulo):
    if angulo == 90:
        angulo = 0
        #return angulo
    elif angulo<90 and angulo>=0:
        angulo=90-angulo
        #return angulo
    elif angulo>90 and angulo<=180:
        angulo=angulo-90
    return angulo
    

def velocidad_ajuste(velocidad):
    if velocidad<77:
        estado='Atras'
    elif velocidad>77:
        estado='Adelante'
    elif velocidad==77:
        estado='Parado'
    velocidad=abs(velocidad-77)
    return velocidad, estado


# Create the window
window = sg.Window("5G RobotCar", layout,size=(900,700),element_justification='c',background_color="white")

while True:
    event, values = window.read(timeout=1)
    window.Refresh()
    velocidad,angulo,deadman,velocidad_max=get_datos()
    velocidad, estado=velocidad_ajuste(velocidad)
    imgVelocidad=img_velocidad(velocidad,velocidad_max)
    imgSemaforo=img_semaforo(deadman)
    img_volante(angulo)
    window['velocidadInterfaz'].Update("V: " + str(round(velocidad,2))+"Km/h " + '\n' + "VMax = " + str(velocidad_max)+" Km/h"+ '\n' + estado )
    window['imgVelInterfaz'].Update(imgVelocidad)
    window['imgSemaforo'].Update(imgSemaforo)
    window['imgVolante'].Update("images\\volante.png")

    if event == sg.WIN_CLOSED:
        break
window.close()