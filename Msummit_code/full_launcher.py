import wheel_module
import threading
import os

class launcher():
    def __init__ (self):
        
        self.usb_port = 0
        self.deadman_port = 1
        self.speedup_port = 3
        self.speeddown_port = 5
        self.throttle_port = 1
        self.brake_port = 2
        self.wheel_port = 0        
        self.controller = wheel_module.PS4Controller(self.usb_port,self.deadman_port,self.speedup_port,self.speeddown_port,self.throttle_port,
                                              self.brake_port,self.wheel_port)
        
  
     

    def start_car(self):
        while True:
            #self.controller.move_car()
            self.controller.dual_send()

        
    def start_GUI(self):
        os.system("python launcher_onlyGUI.py")

        
    def start_program(self):
        GUI=threading.Thread(target=self.start_GUI)
        GUI.start()

        
        car=threading.Thread(target=self.start_car)
        car.start()

        car.join()
        GUI.join()
    
if __name__ == "__main__":       
    launcher = launcher()
    launcher.start_program()