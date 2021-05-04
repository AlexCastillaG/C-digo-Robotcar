import RPi.GPIO as GPIO
import time
import keyboard

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz


def angle_to_percent(angle):
    if angle > 180 or angle < 0:
        return False

    start = 4
    end = 12.5
    ratio = (end - start)/180  # Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent


p.start(angle_to_percent(0))  # Initialization


try:
    while True:

        if keyboard.is_pressed('a'):
            print('a Key was pressed')
            p.ChangeDutyCycle(angle_to_percent(15))

        if keyboard.is_pressed('d'):
            print('d Key was pressed')
            p.ChangeDutyCycle(angle_to_percent(30))

        if keyboard.is_pressed('p'):
            p.stop()
            GPIO.cleanup()
