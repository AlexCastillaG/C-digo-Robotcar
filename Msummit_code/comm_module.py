from distutils.log import error
import socket
import time
from numpy import not_equal

class communicator():

    def __init__(self,filename):
        self.IP,self.PORT,self.BUFFER,self.CHECK = self.get_ip_and_port(filename)
        self.delay = 0.01

    def get_ip_and_port(self,filename):
        with open(str(filename), "r") as a:
            dict = a.read().split(":")
        return dict[0],int(dict[1]),int(dict[2]),bool(int(dict[3]))
        




    
class receiver(communicator):
    
    def __init__(self,filename):
        self.IP,self.PORT,self.BUFFER,self.CHECK = self.get_ip_and_port(filename)
        self.sock = self.create_socket()
        self.delay = 0.01
    
    def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.PORT))
        s.listen(1)
        return s


    def receive(self):
        time.sleep(self.delay)
        conn, addr = self.sock.accept()
        data = conn.recv(self.BUFFER).decode("utf-8")
        data = data.strip('][').split(', ')
        conn.close()
        print(data)
        return data
    
class receiver_raspy(communicator):
    
    def __init__(self,IP,PORT,BUFFER):
        self.IP,self.PORT,self.BUFFER = IP,PORT,BUFFER
        self.sock = self.create_socket()
        self.delay = 0.01
    
    def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.PORT))
        s.listen(1)
        return s


    def receive(self):
        time.sleep(self.delay)
        conn, addr = self.sock.accept()
        data = conn.recv(self.BUFFER).decode("utf-8")
        data = data.strip('][').split(', ')
        conn.close()
        print(data)
        return data
    
class sender(communicator):

    
    def send(self,device_name,*args):  # send the information to a client
        data=[]
        time.sleep(self.delay)
        for n in args:
            data.append(n)
        message = str(data).encode("utf-8")
        
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)     
            self.sock.connect(( self.IP,self.PORT))  
            self.sock.send(message)
            data = self.sock.recv(self.BUFFER)
            self.sock.close()
        except ConnectionRefusedError:
            print("Connection lost: Attempting to reconnect "+"to {}".format(device_name))
        except ConnectionResetError:
            print("Connection lost: Attempting to reconnect "+"to {}".format(device_name))
        #print(data)