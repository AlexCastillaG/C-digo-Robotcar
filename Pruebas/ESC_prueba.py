import keyboard

try:
    while True:

        if keyboard.is_pressed('w'):
            print('w Key was pressed')


        if keyboard.is_pressed('s'):
            print('s Key was pressed')


        if keyboard.is_pressed('p'):
            p.stop()
            GPIO.cleanup()
