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
from datetime import datetime

####### 센서값 핀 할당 #####
button = Button(21)
sensor = DistanceSensor(echo=24, trigger=23)
# 이하 미리 셋업을 해서 시간을 버는 방식
cap = cv2.VideoCapture(0) # 0번 카메라
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# camera = PiCamera()
# camera.resolution = (320, 240)
# camera.rotation = 180
# camera.start_preview()

####### 센서값 핀 할당 끝 #####
####### 서보모터 동작 (pigpio) ########
pi = pigpio.pi()

  
# S3 Client 생성
# s3 = boto3.resource('s3', aws_access_key_id="AKIA53OSENDN4VXRF6JE",
#         aws_secret_access_key="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")
  
# bucket_name = "kf99-mask-image"

CHECK_ZONE = 0.5
PASS_ZONE = 0.2

# def capture_if_innerzone(): #사람위치를 판별하여 클라우드에 사진을 전송함
#     print("begin capture_if_innerzone")
#     global human_distance
#     while True:
#         # if human_distance < CHECK_ZONE and human_distance > PASS_ZONE:
#         if hmn_state == -1 :
#             retval, frame = cap.read()
#             cv2.imwrite("test.jpg",frame)
#             # camera.capture('test.png')
#             # # S3 Bucket 에 파일 업로드 
#             # data = open('test.png', 'rb')
#             # s3.Bucket(bucket_name).put_object(Key='temp_test.png', Body=data)
#             # 여기서 파일 업로드를 함
#             print("captured!",datetime.datetime.now())
#         time.sleep(5)
    
def showtouser(): #이용자에게 화면 보여주면서 사진도 찍는 함수..
    print("True showtouser")
    global human_distance
    global f_path
    past_time = -1
    while True:
        retval, frame = cap.read()
        cv2.imshow('frame', frame)
        # if human_distance < CHECK_ZONE and human_distance > PASS_ZONE:
        ### 5초 간격으로 이미지 파일을 저장 ###
        prnt_time = time.time()
        if (prnt_time - past_time>2):
            fname = datetime.now().strftime("%Y%m%d%H%M%S")
            # print(fname+".jpg")
            f_path = "./image/"+fname+".jpg"
            cv2.imwrite(f_path,frame)
            past_time = prnt_time
            # imgfile = open(f_path, 'rb')
            # r = requests.post("http://3.35.178.102/mask/", files = {'file':imgfile})
            # print(r.text)
            print("captured!")
        key = cv2.waitKey(25)
        if key == 27: break # ESC키를 누른 경우 루프 탈출
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    return 0

# def changestate():
#     global door_state
#     print("state changed!")
#     if door_state == 1:
#         door_state = 0
#     else :
#         door_state = 1
#     print("state is ",door_state)


def mask_check(): #클라우드에서 신호를 받아서 처리하는 곳..
    print("begin mask_check")
    global f_path
    global mask_state
    past_time = -1
    while True:
        prnt_time = time.time()
        if(prnt_time - past_time>1): #간격을 1로 둠
            imgfile = open(f_path, 'rb')
            # res = requests.post("http://3.35.178.102/mask/", files = {'file':imgfile})
            past_time = prnt_time
            print("posted")
            # mask_state = int(res.text)
            # 0 쓴거
            # 1 안쓴거
            # 2 잘못쓴거
            # 4 감지 못한거
            # button.when_pressed = changestate
            # time.sleep(0.5)

# def distance_check():
#     global human_distance
#     while True:
#         human_distance = sensor.distance
#         print(sensor.distance)
#         time.sleep(0.2)

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
def control_door(): #받은 신호와 사람 위치에 따라서 문을 열고 닫는 곳..
    print("begin control_door")
    global hmn_state
    global door_state
    while True:
        if (hmn_state == 1) and (mask_state == 0): # 사람이 포토존에 있고, 마스크를 썼을 경우 door_state = 1
            door_state = 1
        elif(door_state == 1) and((hmn_state == 2)or(hmn_state == 3)): # door_state = 1 이고, 사람이 떠났을 경우 door_state  = 0
            door_state = 0
        else:
            continue

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
human_distance = 0
hmn_state  = -1
door_state = -1
mask_state = -1
f_path = None
# proc = Thread(target=distance_check, args=())
proc1 = Thread(target=human_state_check, args=())
# proc2 = Thread(target=capture_if_innerzone, args=())
proc3 = Thread(target=control_door, args=())
proc4 = Thread(target=mask_check, args=())
proc5 = Thread(target=showtouser, args=())
proc1.start()
# proc2.start()
proc3.start()
proc4.start()
proc5.start()