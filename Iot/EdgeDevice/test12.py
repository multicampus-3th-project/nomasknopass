from gpiozero import Button, DistanceSensor
from picamera import PiCamera
from datetime import datetime
from signal import pause
import time
from threading import Thread
from multiprocessing import Process
import boto3
import pigpio
import cv2
import requests
import os
from datetime import datetime

####### 센서값 핀 할당 #####
button = Button(21)
sensor = DistanceSensor(echo=24, trigger=23)
# 이하 미리 셋업을 해서 시간을 버는 방식
cap = cv2.VideoCapture(0) # 0번 카메라
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
####### 센서값 핀 할당 끝 #####
####### 서보모터 동작 (pigpio) ########
pi = pigpio.pi()

CHECK_ZONE = 0.5
PASS_ZONE = 0.2

def showtouser(): #이용자에게 화면 보여주면서 사진도 찍는 함수..
    print("True showtouser")
    global human_distance
    global f_path
    global imgsaved
    past_time = time.time()
    while True:
        retval, frame = cap.read()
        cv2.imshow('frame', frame)
        # if human_distance < CHECK_ZONE and human_distance > PASS_ZONE: # 사람이 검사존에 있을 경우임
        ### 2초 간격으로 이미지 파일을 저장 ###
        prnt_time = time.time()
        if (prnt_time - past_time>2):
            fname = datetime.now().strftime("%Y%m%d%H%M%S")
            f_path = "./image/"+fname+".jpg"
            cv2.imwrite(f_path,frame)
            print("saved!")
            imgsaved = 1
            past_time = prnt_time
            print("captured!")
        key = cv2.waitKey(25)
        if key == 27: break # ESC키를 누른 경우 루프 탈출
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    return 0

def mask_check(): #클라우드에서 신호를 받아서 처리하는 곳..
    print("begin mask_check")
    global f_path
    global mask_state
    global imgsaved
    past_time = time.time()
    while True:
        lf_path = f_path
        limgsaved = imgsaved
        prnt_time = time.time()
        if(lf_path != None) and (limgsaved == 1): #간격을 1로 둠
            # imgfile = open(lf_path, 'rb')
            # res = requests.post("http://3.35.178.102/mask/", files = {'file':imgfile})
            # res = requests.post(url, files=files, data={"temperature":111}) #이거슨 그.. 온도도 보낼 때
            # imgfile.close()
            # print("posted")

            #여기서 f_path 값에 접근해서 파일 삭제
            try:
                os.remove(lf_path)
                print("deleted")
            except FileNotFoundError:
                print("error occured! filenotError but continue")
                pass
            lf_path = None
            imgsaved = 0
            past_time = prnt_time

            # mask_state = int(res.text)
            # 0 쓴거
            # 1 안쓴거
            # 2 잘못쓴거
            # 4 감지 못한거
            # button.when_pressed = changestate
            # time.sleep(0.5)

def human_state_check():
    print("begin human_state_check")
    global human_distance
    global hmn_state
    prnt_hmn_dist = sensor.distance
    while True:
        time.sleep(0.2)
        human_distance = sensor.distance
        past_hmn_dist = prnt_hmn_dist
        prnt_hmn_dist = sensor.distance
        # print("past:{0:.3f}, prsnt:{1:.3f}".format(past_hmn_dist,prnt_hmn_dist))
        if past_hmn_dist > CHECK_ZONE and prnt_hmn_dist < CHECK_ZONE and prnt_hmn_dist > PASS_ZONE:
            print("human approached")
            hmn_state =  1
        elif past_hmn_dist > PASS_ZONE and prnt_hmn_dist < PASS_ZONE:
            print("human passed")
            hmn_state = 2
        elif past_hmn_dist < CHECK_ZONE and prnt_hmn_dist > CHECK_ZONE and past_hmn_dist > CHECK_ZONE:
            print("human returned")
            hmn_state = 3
        else:
            continue

# sudo pigpiod
def control_door(): #받은 신호와 사람 위치에 따라서 문을 열고 닫는 곳+사람에게 안내하는 곳..
    print("begin control_door")
    global hmn_state
    global door_state
    past_time = time.time()
    while True:
        prnt_noticed = time.time()
        if (prnt_noticed-past_time)>3: #3초간격 실행슨
            if (hmn_state == 1) and (mask_state == 0): # 사람이 포토존에 있고, 마스크를 썼을 경우 door_state = 1
                door_state = 1
                print("빨리 지나가세요")
            elif(door_state == 1) and((hmn_state == 2)or(hmn_state == 3)): # door_state = 1 이고, 사람이 떠났을 경우 door_state  = 0
                door_state = 0
                print("door closed")
            elif (door_state == 1) and (hmn_state == 1) and ((mask_state == 2) or (mask_state == 1)):#사람이 포토존에 있고, 마스크를 잘못 썼을 경우(/이미 문이 열린 경우)
                print("가기전에 고쳐 쓰세요")
            elif (door_state == 0) and (hmn_state == 1) and (mask_state == 2): #사람이 포토존에 있고, 마스크를 잘못 썼을 경우 (/문이 열리지 않은 경우)
                print("고쳐쓰세요")
            elif (door_state == 0) and (hmn_state == 1) and (mask_state == 3): #사람이 포토존에 있고, 마스크를 안 썼을 경우
                print("돌아가라")
            else:
                continue
            past_noticed = prnt_noticed 

        if (door_state == 1):
            pi.set_servo_pulsewidth(25, 600)
        elif(door_state == 0): #door_state == 0
            pi.set_servo_pulsewidth(25, 2400)
        else:
            continue
    return 0

global human_distance
global hmn_state
global door_state
global f_path
global mask_state
global imgsaved

human_distance = 0
hmn_state  = -1
door_state = 0
f_path = None
mask_state = -1
imgsaved = 0

proc1 = Thread(target=human_state_check, args=())
proc3 = Thread(target=control_door, args=())
proc4 = Thread(target=mask_check, args=())
proc5 = Thread(target=showtouser, args=())
proc1.start()
proc3.start()
proc4.start()
proc5.start()