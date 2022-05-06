import comm_module
import time 


receiver = comm_module.receiver_raspy("",5009,1024)

while True:
    time.sleep(0.01)
    receiver.receive()