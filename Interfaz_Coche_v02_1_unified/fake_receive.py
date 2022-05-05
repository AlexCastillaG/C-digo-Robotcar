import socket
import json

TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

def receive(s):
    try:
        conn, addr = s.accept()
        data= conn.recv(BUFFER_SIZE).decode("utf-8")
        fiveg_data= json.loads(data)
        conn.close()
        fiveg_connect=True
    except:
        raise

        
    return fiveg_data

while True:
        
    message = receive(s)
    print(message)