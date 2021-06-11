import threading

 
class ThreadClass_Throttle(threading.Thread):
    
  def run(self):
    while True:
        print("ThreadClass_PS4")
 
class ThreadClass_PS4(threading.Thread):
    
  def run(self):
    while True:      
        print("ThreadClass_Throttle")



hiloPS4 = ThreadClass_Throttle()
hiloPS4.start()

hiloThrottle = ThreadClass_PS4()
hiloThrottle.start()




