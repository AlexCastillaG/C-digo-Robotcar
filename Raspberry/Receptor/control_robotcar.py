#Imports
import time
import sys, tty, termios
import pigpio
import RPi.GPIO as GPIO

#defs
def angle_to_percent(angle):
    if angle > 180 or angle < 0:
        return False

    start = 4
    end = 12.5
    ratio = (end - start)/180  # Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

def initialization():

    pwm.start(angle_to_percent(0))
    
    pi.set_servo_pulsewidth(ESC, 0)

    pi.set_PWM_frequency(ESC,100)

    pi.set_servo_pulsewidth(ESC,2000)

    pi.set_servo_pulsewidth(ESC,1000)

    pi.set_servo_pulsewidth(ESC,1500)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def turn_l():
    print('Turning left')
    pwm.ChangeDutyCycle(angle_to_percent(20))
    pwm.set_PWM_dutycycle(pwm_gpio,0)
def turn_r():
    print('Turning rigth')
    pwm.ChangeDutyCycle(angle_to_percent(120))º1º
def turn_0():
    print('Straigth forward')
    pwm.ChangeDutyCycle(angle_to_percent(90))
    
def accelerate(actual_vel):

    actual_vel=actual_vel+10
    turn_0()
    pi.set_servo_pulsewidth(ESC,actual_vel)
    print('accelerating actual_speed:{}'.format(actual_vel))
    return actual_vel
def deccelerate(actual_vel):
    actual_vel=actual_vel-10
    pi.set_servo_pulsewidth(ESC,actual_vel)
    print('decelerating actual_speed:{}'.format(actual_vel))
    return actual_vel
#connections, vars and pins
ESC = 13


GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings


#Use pin 12 for PWM signal
pwm_gpio = 12
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)



pi = pigpio.pi() # Connect to local Pi.



#main

initialization()

vel = 1500

while True:
    
    char=getch()
    
    if char=='w':
        
        turn_0()
        vel=accelerate(vel)
    
    elif char=='a':
    
        turn_l()
    
    elif char=='s':
    
        vel=deccelerate(vel)
    
    elif char=='d':
        
        turn_r()
    
    else:
        exit()

