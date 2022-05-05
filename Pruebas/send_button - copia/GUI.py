import PySimpleGUI as sg
import socket



def sendInterfaz(check):
  
    sock = socket.socket(socket.AF_INET,  # Internet
                                socket.SOCK_STREAM)  # TCP
    sock.connect(("localhost",5050))
    sock.send(check)
    data = sock.recv(1024)
    sock.close()

layout = [[sg.Checkbox('Conectar', default=False,enable_events = True)],[sg.Text("",key="-text-")]]
window = sg.Window("5G RobotCar", layout,size=(900,700),element_justification='c',background_color="white")

while True:
    event, values = window.read(timeout=1)

    window.Element("-text-").Update(value=values.get(0))
    sendInterfaz(str(values.get(0)).encode("utf-8"))
    
    if event == sg.WIN_CLOSED:
        break
window.close()