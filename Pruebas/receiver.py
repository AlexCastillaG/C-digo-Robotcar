import socket

UDP_IP = ""
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(("", UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    message= json.loads(data.decode())
    print("speed: %s"% message.get("speed")+" angle: %s"% message.get("angle"))





