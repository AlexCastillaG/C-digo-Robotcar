import socket
import time

host = '127.0.0.1'
port = 8050
i=0

 
def send(input_palanca): #send the information to a client
    
    try:
        input_palanca=(input_palanca-1)/2

        MESSAGE = bytes(str(input_palanca), encoding = "utf-8")


        sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_STREAM)  # TCP
        sock.connect((host,port))
        sock.send(MESSAGE)
        data = sock.recv(1024)
        sock.close()
        print(input_palanca)
    except:
        print("fallo de conexion")
        
while True:
    i=i+2
    send(i)
    time.sleep(0.5)
    print(i)