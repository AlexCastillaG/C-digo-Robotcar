
def get_ip_and_port():
    with open("ip_and_port.txt", "r") as a:
       dict = a.read().split(":")
    return dict[0],int(dict[1]),bool(int(dict[2]))



print (get_ip_and_port())