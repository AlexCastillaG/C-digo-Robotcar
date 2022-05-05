import time,threading

def prueba_multi_1():
        print("Programa 1 se ejecuta a las: ",time.ctime(time.time()))

def prueba_multi_2():
        print("Programa 2 se ejecuta a las: ",time.ctime(time.time()))        
        
        
def start_program():
        car=threading.Thread(target=prueba_multi_1())
        car.start()

        GUI=threading.Thread(target=prueba_multi_2())
        GUI.start()


        car.join()
        GUI.join()
while True:
    start_program()