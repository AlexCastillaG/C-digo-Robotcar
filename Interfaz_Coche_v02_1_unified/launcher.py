import os
import threading
import volante
import Interfaz2

def run_volante():
    print("car_mvin")
    ps4 = volante.PS4Controller
    ps4.init(ps4)
    ps4.listen(ps4) 
    
def run_interfaz():
    print("gui_mvin")
    Interfaz2.exect_GUI()

def start_program():
    volante=threading.Thread(target=run_volante)
    volante.start()

    interfaz=threading.Thread(target=run_interfaz)
    interfaz.start()


    volante.join()
    interfaz.join()
 



#####################MAIN#######################

if __name__ == "__main__":
    start_program()