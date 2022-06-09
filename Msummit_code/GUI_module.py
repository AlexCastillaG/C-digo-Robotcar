import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Titlebar, Window
from PIL import Image
import comm_module

class Interface():
    
    def __init__(self,layout,window):
        self.layout = layout
        self.window = window
        
    def start_GUI(self):
        while True:
            event, values = self.window.read()
            self.window.Refresh()
            if event == sg.WIN_CLOSED:
                break
        self.window.close()
        
class car_Interface(Interface):



    def __init__(self):        
        self.speed = 0.0
        self.max_speed = 5
        self.angle = 0.0
        self.error_code = "System OK"
        self.deadman = False
        self.state = "Stop"
        self.data_receiver = comm_module.tcp_request(1024,"CONF_GUI.txt")
        self.speed_images = ["images\\velocidad_PARADO.png","images\\velocidad_1.png","images\\velocidad_2.png","images\\velocidad_3.png",
                                    "images\\velocidad_4.png","images\\velocidad_5.png","images\\velocidad_6.png","images\\velocidad_MAX.png"]
        self.speed_img = self.speed_images[0]
        self.wheel_img = "images\\volante_original.png"
        self.deadman_img = "images\semaforo_rojo.png"
        col_21 =[
            [sg.Image(self.speed_img,key="speed_img",size=(200,200),background_color="white")],
            [sg.Text(text="Maximum Gas: {}%\nCurrent Speed: {} km/h\nDirection: {}".format(self.max_speed,self.speed,self.state),justification="l",background_color="white",text_color="black",key="GUI_data",font=('Helvetica', 20)),sg.Push(background_color="white")]
            ]
        col_22 =[
            [sg.Push(background_color="white"),sg.Image(self.deadman_img,key="deadman_img",size=(200,150),background_color="white"),sg.Push(background_color="white")],
            [sg.Push(background_color="white"),sg.Text(text="System Status:",justification="l",background_color="white",text_color="black",font=('Helvetica', 20)),sg.Push(background_color="white")],   
            [sg.Multiline(default_text=self.error_code,size=(30,5),auto_refresh=True,enable_events=True)]
            ]
            
        self.layout = [[sg.Image("images\logoiteam.png",size=(512,170),background_color="white")],
                    [ sg.Frame(layout=col_22, border_width=0,title='',background_color="white"),
                        sg.Image(self.wheel_img,key="wheel_img",size=(800,800),background_color="white"),
                        sg.Frame(layout=col_21, border_width=0,title='',background_color="white")]]
  
        
        self.window = sg.Window("5G RobotCar", self.layout,resizable=True,size=(1920,1080),element_justification='c',background_color="white")
        self.layout = self.layout
        self.window = self.window.Finalize()
        self.window.Maximize()
        
        
    def get_data(self):
        speed,angle  = self.data_receiver.request()
        deadman = True
        max_speed = 2000
        self.speed = round(float(speed),1)
        self.angle = round(float(angle),1)
        self.deadman = deadman
        self.max_speed = int(max_speed)
        
            
    def switch_wheel_img(self):
        self.angle=int(self.angle-90)
        im = Image.open('images\\volante_original.png')
        im=im.rotate(self.angle)
        im.save('images\\volante.png')
        im.close()          
    
    def get_speed_img (self):
        
        self.max_speed = round(float(self.max_speed/7),1)

        if self.speed==0:
            self.speed_img = self.speed_images[0]

        elif self.speed>0 and self.speed <= self.max_speed:
            self.speed_img = self.speed_images[1]

        elif self.speed>self.max_speed and self.speed <= 2*self.max_speed:
            self.speed_img = self.speed_images[2]

        elif self.speed>2*self.max_speed and self.speed <= 3*self.max_speed:
            self.speed_img = self.speed_images[3]

        elif self.speed>3*self.max_speed and self.speed <= 4*self.max_speed:
            self.speed_img = self.speed_images[4]

        elif self.speed>4*self.max_speed and self.speed <= 5*self.max_speed:
            self.speed_img = self.speed_images[5]

        elif self.speed>5*self.max_speed and self.speed <= 6*self.max_speed:
            self.speed_img = self.speed_images[6]
            
        elif self.speed>6*self.max_speed:
            self.speed_img = self.speed_images[7]
            
        else: 
            self.speed_img = self.speed_images[0]  
            
    def get_deadman_img(self):
        if self.deadman == "True":
            self.deadman_img = "images\semaforo_verde.png"
        else: 
            self.deadman_img = "images\semaforo_rojo.png"

    def speed_adjusting(self):
        if self.speed<77.00:
            self.state='Backward'
        elif self.speed>77.00:
            self.state='Forward'
        elif self.speed==77.00:
            self.state='Stop'
        self.speed=abs(self.speed-77.00)

          
           
    def start_GUI(self):
        while True:
            event, values = self.window.read(timeout=500)
            print(self.get_data())  
            """         
            self.speed_adjusting()
            self.get_speed_img()
            self.get_deadman_img()
            self.switch_wheel_img()         
            self.window['GUI_data'].Update("Maximum Gas: {}%\nCurrent Speed: {} km/h\nDirection: {}".format(self.max_speed,self.speed,self.state ))
            self.window['speed_img'].Update(self.speed_img)
            self.window['deadman_img'].Update(self.deadman_img)

            self.window['wheel_img'].Update("images\\volante.png")
            self.window.Refresh()
            """

            #print(self.speed,self.angle,self.deadman,self.max_speed)
            if event == sg.WIN_CLOSED:
                break
        self.window.close()
        