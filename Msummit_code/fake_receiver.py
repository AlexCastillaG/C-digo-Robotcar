import comm_module
import time 

fake_receiver = comm_module.receiver("control_netinfo.txt")

while True:
    time.sleep(0.01)
    fake_receiver.receive()