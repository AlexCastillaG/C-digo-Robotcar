import keyboard



while True:
# Check if b was pressed
    if keyboard.is_pressed('w'):
        print('w Key was pressed')
        
    if keyboard.is_pressed('a'):
        print('a Key was pressed')

    if keyboard.is_pressed('s'):
        print('s Key was pressed')

    if keyboard.is_pressed('d'):
        print('d Key was pressed')

    if keyboard.is_pressed("p"):
        quit()