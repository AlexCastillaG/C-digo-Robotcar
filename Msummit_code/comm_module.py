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

    def decode_data(self,data):
        data = data.decode("utf-8").strip('][').split(', ')
        return data



    
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
        data = conn.recv(self.BUFFER)
        data = self.decode_data(data)
        conn.close()
        print(data)
        return data
    
class server(communicator):
    
    def __init__(self,IP,PORT,BUFFER):
        self.IP,self.PORT,self.BUFFER = IP,PORT,BUFFER

    
    def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.PORT))
        s.listen(1)
        conn, addr = s.accept()
        return conn
    
    def send(self):
        while True:
            self.conn = self.create_socket()
            i=0
            while True:
                self.delay = 0.01
                data = self.conn.recv(self.BUFFER)
                message = self.decode_data(data)
                print("received: " , message)
                if not data:
                    break
                i=i+1
                data = i
                print("sending :" , data)
                self.conn.sendall(str(data).encode("utf-8"))
            self.conn.close()
        
class tcp_request(communicator):
    
    def __init__(self,IP,PORT,BUFFER):
        self.IP,self.PORT,self.BUFFER = IP,PORT,BUFFER
        self.data="hello"
        
    def create_socket(self):  
      
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.s.connect((self.IP, self.PORT))
                break
            except socket.error:
                self.s.close()
                print("El control esta desconectado")
                continue
            
    def request(self):
        
        self.create_socket()


        time.sleep(0.01)
        message = str(self.data).encode("utf-8")
        print("sending: " , message)
        try:
            self.s.sendall(message)
            self.data = self.decode_data(self.s.recv(self.BUFFER))
        except socket.error:
            print("Se cerro el programa de control durante la trasmision")
            self.s.close()
            self.create_socket()
        print("receiving:" , self.data)
        #print("echo: ",data)
        return self.data

class sender(communicator):

    
    def send(self,device_name,*args):  # send the information to a client
        data=""
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
            print("Devices has been disconnected "+"from {}".format(device_name))
        except TimeoutError:
            print("Devices has been disconnected for too long, reconnect or quit the program")
        except OSError:
            print("There is no connection available, connect to the rigth router")
        except Exception as e:
            print("Unknown error: " , e)
            
        #print(data)
            


