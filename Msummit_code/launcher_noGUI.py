import wheel_module
import time


usb_port = 0
deadman_port = 1
speedup_port = 3
speeddown_port = 5
throttle_port = 1
brake_port = 2
wheel_port = 0

PS4 = wheel_module.PS4Controller(usb_port,deadman_port,speedup_port,speeddown_port,throttle_port,brake_port,wheel_port)
while True:
    try:
        PS4.move_car()
        #PS4.mapping_tool()
    except OSError:
        print("El dispositivo con IP ",PS4.control_sender.addr[0], "y puerto ",PS4.control_sender.addr[1], "se desconecto")
        PS4 = wheel_module.PS4Controller(usb_port,deadman_port,speedup_port,speeddown_port,throttle_port,brake_port,wheel_port)
        continue