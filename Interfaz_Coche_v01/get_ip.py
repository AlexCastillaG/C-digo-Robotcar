
def get_ip_and_port():
    with open("ip_and_port.txt", "r") as a:
       dict = a.read().split(":")
    return {"ip":dict[0],"port":int(dict[1])}

print (get_ip_and_port())