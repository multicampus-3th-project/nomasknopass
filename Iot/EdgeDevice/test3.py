from gpiozero import DistanceSensor, Button
from threading import Thread
import time
import cv2
import boto3
import os
from datetime import datetime
from signal import pause
import time

CHECK_ZONE = 0.5
PASS_ZONE = 0.2
button = Button(21)

sensor = DistanceSensor(echo=24, trigger=23)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 460)
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

def human_waytogo():
    global hmn_state
    prnt_hmn_dist = sensor.distance
    while True:
        time.sleep(0.2)
        past_hmn_dist = prnt_hmn_dist
        prnt_hmn_dist = sensor.distance
        if (past_hmn_dist>PASS_ZONE and prnt_hmn_dist < PASS_ZONE and prnt_hmn_dist > 0 ):
            print("human passed")
            hmn_state = 1
        elif (past_hmn_dist<CHECK_ZONE and prnt_hmn_dist > CHECK_ZONE):
            print("human returned")
            hmn_state = 2
        elif (past_hmn_dist>CHECK_ZONE and prnt_hmn_dist < CHECK_ZONE and prnt_hmn_dist > PASS_ZONE ):
            print("human approached")
            hmn_state = 3
        else :
            continue
        print("distance {0:.4f}, and state {0:.d}".format(sensor.distance, hmn_state))
def white_rectangle(frame):
    cv2.rectangle(frame, (int(cap_width/4),int(cap_height/6)),(int(cap_width*3/4),int(cap_height*5/6)), (255, 255, 255), 2)
def green_rectangle(frame):
    cv2.rectangle(frame, (int(cap_width/4),int(cap_height/6)),(int(cap_width*3/4),int(cap_height*5/6)), (0, 255, 0), 2)
def yello_rectangle(frame):
    cv2.rectangle(frame, (int(cap_width/4),int(cap_height/6)),(int(cap_width*3/4),int(cap_height*5/6)), (0, 255, 255), 2)


def photo_check():
    global hmn_state
    global mask_state 
    while True:
        retval, frame = cap.read() # 프레임 캡처
        if not retval: break
        if hmn_state == 3:
            if mask_state == 1:
                green_rectangle(frame)
            elif mask_state == 2:
                yello_rectangle(frame)
            else :
                white_rectangle(frame)
        frame=cv2.flip(frame,1)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(25)
        if key == 27: break # ESC키를 누른 경우 루프 탈출
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()

def distance_check():
    while True:
        print('Distance: ', sensor.distance * 100)
        time.sleep(5)

def img_send(cap):
    global hmn_state
    global mask_state
    while True:
        if hmn_state == 3:
            capture(cap)
        time.sleep(0.2)

def mask_confirmed():
    print("hmn_state is 1!")

def mask_default():
    print("hmn_state is 0!")

def mask_check():
    while True:
        button.when_pressed = mask_confirmed
        button.when_released = mask_default
        if hmn_state == 1:
            print("you passed")
        elif hmn_state == 2:
            print("you cannot passed")
        else:
            continue
        time.sleep(0.2)


def capture(cap):
    timestamp = datetime.now().isoformat()
    cap.capture('/home/pi/%s.jpg' % timestamp)
    print("captured!")
     
if __name__ == "__main__":
    global past_hmn_dist
    global prnt_hmn_dist
    global hmn_state
    global mask_state
    mask_state = 2
    hmn_state = 3 #일단 진행 절차상 3으로..
    proc = Thread(target=photo_check, args=())
    proc3 = Thread(target=mask_check, args=())
    proc2 = Thread(target=human_waytogo, args=())
    proc.start()
    proc2.start()
    proc3.start()
    while True:
        print('Distance: ', sensor.distance * 100)
        time.sleep(2)
    

    #사진 송신 메소드
    #판단 수신 메소드
    #거리 접근 메소드
     # 사람이 범주 내에 있다