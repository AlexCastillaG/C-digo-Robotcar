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
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.delay = 0.01
    
    def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.PORT))
        s.listen(1)
        return s

        
    def receive(self):
        time.sleep(self.delay)
        conn, addr = self.sock.accept()
        try:
            print('client connected:', addr)
            while True:
                data = conn.recv(1024)
                print('received {!r}'.format(data))
                if data:
                    conn.sendall(data)
                else:
                    break
        finally:
            conn.close()
    
class tcp_sender(communicator):
    def send(self,device_name,*args):
        sock = socket.create_connection(( self.IP,self.PORT))
        try:
            message=[]
            time.sleep(self.delay)
            for n in args:
                message.append(n)
            print('sending {!r}'.format(message))
            
            sock.sendall(str(message).encode("utf-8"))

            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = sock.recv(1024)
                amount_received += len(data)
                print('received {!r}'.format(data))
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
            print("Devices has been disconnected "+"from {}".format(device_name))
        except TimeoutError:
            print("Devices has been disconnected for too long, reconnect or quit the program")
        except OSError:
            print("There is no connection available, connect to the rigth router")
        except Exception as e:
            print("Unknown error: " , e)
            
        #print(data)