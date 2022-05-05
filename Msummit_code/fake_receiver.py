import comm_module
import time 

fake_receiver = comm_module.sender("control_netinfo.txt")
fake_receiver.IP="127.0.0.1"

while True:
    time.sleep(0.01)
    fake_receiver.send("raspy")