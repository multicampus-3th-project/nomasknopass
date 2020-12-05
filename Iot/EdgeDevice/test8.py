import pigpio
from time import sleep
pi = pigpio.pi()
while True:
        pi.set_servo_pulsewidth(25, 600)
        sleep(1)
        pi.set_servo_pulsewidth(25, 1500)
        sleep(1)
        pi.set_servo_pulsewidth(25, 2400)
        sleep(1)  