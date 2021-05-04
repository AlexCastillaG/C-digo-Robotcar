1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time
 
servo = 23
 
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
 
pwm.set_PWM_frequency( servo, 50 )
 
print( "0 deg" )
pwm.set_servo_pulsewidth( servo, 500 ) ;
time.sleep( 3 )
 
print( "90 deg" )
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 3 )
 
print( "180 deg" )
pwm.set_servo_pulsewidth( servo, 2500 ) ;
time.sleep( 3 )
 
# turning off servo
pwm.set_PWM_dutycycle(servo, 0)
pwm.set_PWM_frequency( servo, 0 )