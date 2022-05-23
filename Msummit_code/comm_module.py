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
    
class receiver_raspy(communicator):
    
    def __init__(self,IP,PORT,BUFFER):
        self.IP,self.PORT,self.BUFFER = IP,PORT,BUFFER

    
    def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.PORT))
        s.listen(1)
        conn, addr = s.accept()
        return conn

        
    def receive(self):
        self.conn = self.create_socket()
        while True:
            self.delay = 0.01
            data = self.conn.recv(self.BUFFER)
            message = self.decode_data(data)
            print(message)
            if not data:
                break
            self.conn.sendall(data)
        self.conn.close()
    
class tcp_sender(communicator):
    
    def __init__(self,IP,PORT,BUFFER):
        self.IP,self.PORT,self.BUFFER = IP,PORT,BUFFER
        self.data=[]
        
    def create_socket(self):  
      
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.IP, self.PORT))      
      
    def send(self,device_name,*args):
        
            self.delay = 0.01
            try:
                data=[]
                time.sleep(self.delay)
                for n in args:
                    data.append(n)
                message = str(data).encode("utf-8")            
                self.s.sendall(message)
                data = self.s.recv(self.BUFFER)
                #print("echo: ",data)
                
            except ConnectionRefusedError:
                print("Connection lost: Attempting to reconnect "+"to {}".format(device_name))
                self.s.close()
            except ConnectionResetError:
                print("Devices has been disconnected "+"from {}".format(device_name))
                self.s.close()
            except TimeoutError:
                print("Devices has been disconnected for too long, reconnect or quit the program")
                self.s.close()
            except OSError:
                print("There is no connection available, connect to the rigth router")
                self.s.close()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("Unknown error: " , e)
                self.s.close()
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
            
if __name__=="__main__":
    sender = tcp_sender("127.0.0.1",5009,1024)
    sender.send("Prueba","message 1")

