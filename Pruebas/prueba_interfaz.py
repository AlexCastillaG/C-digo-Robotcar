import tkinter as tk
import datetime
import socket
import time
from tkinter.constants import NW
import PIL
from PIL import ImageTk
from PIL import Image

#server_palanca = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_palanca.bind(("127.0.0.1", 8050))
#server_palanca.listen(1)

class Test():
    
    def __init__(self):

        self.root = tk.Tk()
        #self.motor1 = tk.Label(self.root, text="Text")
        self.root.geometry('600x400')
        
        
        
        self.root.resizable(width=False,height=False)
        self.root.title('Laser 5G')
        
        
        canvas = tk.Canvas(self.root, width=500,height=150)
        canvas.pack(side="top")
        img = tk.ImageTk.PhotoImage(tk.Image.open("logoiteam.png"))
        canvas.create_image(10,10,anchor=NW,image=img)   

        canvas2 = tk.Canvas(self.root, width=140,height=220)
        canvas2.pack(side="bottom")
        img2 = tk.ImageTk.PhotoImage(tk.Image.open("barco.png"))
        canvas2.create_image(40,10,anchor=NW,image=img2) 
        
        
        
        
        
        """       
    def changeText(self):
        self.motor1.configure(text=str(self.get_palanca()))   
        self.root.after(100, self.changeText) 
         
        
        
    def get_palanca(self):
        
        cli, addr =server_palanca.accept()
        dato = cli.recv(1024).decode("ascii")
        cli.close()
        return dato
        """
        #self.button = tk.Button(self.root,
         #                       text="Click to change text below")
        
        #self.button.pack()
        #self.motor1.pack()
        #self.changeText()
        self.root.mainloop()

 
        
app=Test()

