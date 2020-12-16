import pigpio
import time
pi = pigpio.pi()
while True:
        # pi.set_servo_pulsewidth(25, 600)
        # sleep(1)
        # pi.set_servo_pulsewidth(25, 1500)
        # sleep(1)
        # pi.set_servo_pulsewidth(25, 2000)
        # sleep(1)
        for step in range (100):
                pi.set_servo_pulsewidth(25, 600+8*step)
                time.sleep(0.01)
        time.sleep(1)
        for step in range (100):
                pi.set_servo_pulsewidth(25, 1400-8*step)
                time.sleep(0.01)
        time.sleep(1)