import os
import threading

def run_volante():
    os.system('python3 volante.py')
    
def run_interfaz():
    os.system('python3 Interfaz2.py')

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