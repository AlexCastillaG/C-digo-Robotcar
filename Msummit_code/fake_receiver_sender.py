import comm_module
import time 


sender = comm_module.sender("control_netinfo_receiver.txt")

while True:
    time.sleep(0.01)
    sender.send("raspy",[1500,int(input("angle: "))])