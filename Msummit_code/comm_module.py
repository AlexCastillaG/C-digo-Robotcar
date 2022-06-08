from distutils.log import error
import socket
import time
from numpy import not_equal
import traceback
class communicator():

    def __init__(self,filename):
        self.IP,self.PORT,self.BUFFER,self.CHECK = self.get_ip_and_port(filename)
        self.delay = 0.01

    def get_ip_and_port(self,filename):
        with open(str(filename), "r") as a:
            dict = a.read().split(":")
        return dict[0],int(dict[1]),int(dict[2]),bool(int(dict[3]))

    def decode_data(self,data):
        data = data.decode("utf-8").strip('][').split(', ')
        return data


    
class server(communicator):
    
    def __init__(self,IP,PORT,BUFFER):
        self.IP,self.PORT,self.BUFFER = IP,PORT,BUFFER
        self.conn = self.create_socket()
        self.data = None
    
    def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.PORT))
        s.listen(1)
        conn, self.addr = s.accept()
        conn.settimeout(2)
        print("Se conecto un nuevo dispositivo con ip ",self.addr[0], " por el puerto ",self.addr[1])
        return conn
    

    def send(self,*args):
        time.sleep(0.01)
        to_send_data = [] 
        for item in args:
            to_send_data.append(item)
        self.data = self.conn.recv(self.BUFFER)

        if not self.data:
            to_send_data = []
            print("No se recibieron datos del dispositivo con ip ",self.addr[0], " y puerto ",self.addr[1])
            self.conn.close()

            
        self.data = to_send_data
        #print("sending :" , data)
        self.conn.sendall(str(self.data).encode("utf-8"))
        
class tcp_request(communicator):
    
    def __init__(self,IP,PORT,BUFFER):
        self.IP,self.PORT,self.BUFFER = IP,PORT,BUFFER
        self.data="hello"
        self.create_socket()

        
    def create_socket(self):  
   
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(0.5)
        self.s.connect((self.IP, self.PORT))

    def close_connection(self):
        self.s.close()
        
    def request(self):

        time.sleep(0.01)
        message = str(self.data).encode("utf-8")
        self.s.sendall(message)
        self.data = self.decode_data(self.s.recv(self.BUFFER))
        return self.data


            


