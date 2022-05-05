import comm_module

receiver = comm_module.receiver("control_netinfo_receiver.txt")

receiver.IP = "127.0.0.1"
while True:
    print(receiver.receive())