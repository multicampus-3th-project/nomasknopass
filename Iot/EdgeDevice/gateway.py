from gpiozero import Button, DistanceSensor
from picamera import PiCamera
from datetime import datetime
from signal import pause
import time
from threading import Thread
from multiprocessing import Process
import pigpio
import cv2
import requests
import os
from datetime import datetime
from pydub.playback import play
import spidev
from smbus2 import SMBus
from mlx90614 import MLX90614
import time

####### 센서값 핀 할당 #####
button = Button(21)
# 이하 미리 셋업을 해서 시간을 버는 방식
cap = cv2.VideoCapture(0) # 0번 카메라
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
####### 센서값 핀 할당 끝 #####
####### 서보모터 동작 (pigpio) ########
pi = pigpio.pi()

CHECK_ZONE = 0.4 #voltage 기준
PASS_ZONE = 1.9


spi = spidev.SpiDev()
spi.open(0,0) # (버스, 디바이스)
spi.mode = 3
spi.max_speed_hz = 1000000

####MLX90614#####
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)


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
        if (prnt_time - past_time>2) and hmn_state == 1:
            fname = datetime.now().strftime("%Y%m%d%H%M%S")
            f_path = "./image/"+fname+".jpg"
            cv2.imwrite(f_path,frame)
            # print("saved!")
            imgsaved = 1
            past_time = prnt_time
            #print("captured!")
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
    global hmn_temp
    past_time = time.time()
    while True:
        lf_path = f_path
        limgsaved = imgsaved
        prnt_time = time.time()
        lhmn_temp = 36.5
        if prnt_time-past_time > 0.5 and (lf_path != None) and (limgsaved == 1) and lhmn_temp > 30: #간격을 1로 둠
            try:
                imgfile = open(lf_path, 'rb')
                # res = requests.post("http://3.35.178.102/mask/", files = {'file':imgfile})
                res = requests.post('http://3.35.178.102/predictmask/', files={'image':imgfile}, data={"temperature":lhmn_temp}) #이거슨 그.. 온도도 보낼 때
                #print(lhmn_temp)
                imgfile.close()
                print("posted")
                #여기서 f_path 값에 접근해서 파일 삭제
                try:
                    os.remove(lf_path)
                    # print("deleted")
                except FileNotFoundError:
                    print("delete error occured! filenotError but continue")
                    pass
                try:
                    mask_state = res.json()['mask']
                except:
                    print("OrdinaryJSONDecodeError")
                    pass
            except FileNotFoundError:
                print("open error occured! filenotError but continue")
            #     pass
            # if   mask_state == 0:# 0 쓴거
            #     print("yesMasked")
            # elif mask_state == 1:# 1 안쓴거
            #     print("noMasked")
            # elif mask_state == 2:# 2 잘못쓴거
            #     print("wrongMasked")
            # elif mask_state == 4:# 4 감지 못한거
            #     print("maskNotFound")
            # else:
            #     pass
            lf_path = None
            imgsaved = 0
            past_time = prnt_time

def analog_read(channel):
    # 매개변수 (시작비트, 채널, 자릿수 맞춤 위치), 리턴값 : 아날로그 값
    r = spi.xfer2([1, (0x08+channel)<<4, 0])
    adc_out = ((r[1]&0x03)<<8) + r[2] # 수신 데이터 결합
    return adc_out

def human_state_check():
    print("begin human_state_check")
    global hmn_state
    global hmn_dist
    prnt_hmn_dist = 0
    past_hmn_dist = 0
    while True:
        adc = analog_read(0)
        prnt_hmn_dist = adc*3.3/1023 #voltage type
        # print("Voltage = %.4fV" % (voltage))
        time.sleep(0.75)
        # print("past:{0:.3f}, prsnt:{1:.3f}".format(past_hmn_dist,prnt_hmn_dist))
        if past_hmn_dist < CHECK_ZONE and prnt_hmn_dist > CHECK_ZONE and prnt_hmn_dist < PASS_ZONE:
            print("human approached")
            hmn_state =  1
        elif past_hmn_dist < PASS_ZONE and prnt_hmn_dist > PASS_ZONE and hmn_state == 1:
            print("human passed")
            res = requests.post('http://3.35.178.102/ispass/',data={"ispass":1})
            hmn_state = 2
        elif past_hmn_dist > CHECK_ZONE and prnt_hmn_dist < CHECK_ZONE and past_hmn_dist < PASS_ZONE and hmn_state == 1:
            print("human returned")
            res = requests.post('http://3.35.178.102/ispass/',data={"ispass":0})
            hmn_state = 3
        else:
            pass
        past_hmn_dist = prnt_hmn_dist
        

# sudo pigpiod
def control_door(): #받은 신호와 사람 위치에 따라서 문을 열고 닫는 곳+사람에게 안내하는 곳..
    print("begin control_door")
    global hmn_state
    global door_state
    past_noticed = time.time()
    is_judged = 0
    while True:
        prnt_noticed = time.time()
        if (prnt_noticed-past_noticed)>0.5: #0.5초간격 실행슨
            if (hmn_state == 1) and (mask_state == 0) and (is_judged == 0): # 사람이 포토존에 있고, 마스크를 썼을 경우 door_state = 1
                door_state = 1
                is_judged = 1
                print("you can pass")
                #play("./sound/passed.mp3")
            elif(door_state == 1) and((hmn_state == 2)or(hmn_state == 3)) and (is_judged == 1): # door_state = 1 이고, 사람이 떠났을 경우 door_state  = 0
                door_state = 0
                is_judged = 0
                print("door closed")
                #play("./sound/closed.mp3")
            elif (door_state == 1) and (hmn_state == 1) and ((mask_state == 2) or (mask_state == 1)) and (is_judged == 0):#사람이 포토존에 있고, 마스크를 잘못 썼을 경우(/이미 문이 열린 경우)
                print("wrong masked")
                #play("./sound/wrong.mp3")
            elif (door_state == 0) and (hmn_state == 1) and (mask_state == 2): #사람이 포토존에 있고, 마스크를 잘못 썼을 경우 (/문이 열리지 않은 경우)
                print("wrong masked")
                #play("./sound/wrongclosed.mp3")
            elif (door_state == 0) and (hmn_state == 1) and (mask_state == 3): #사람이 포토존에 있고, 마스크를 안 썼을 경우
                print("return")
                #play("./sound/nomask.mp3")
            else:
                pass
            if (door_state == 1):
                pi.set_servo_pulsewidth(25, 600)
            elif(door_state == 0): #door_state == 0
                pi.set_servo_pulsewidth(25, 2000)
            else:
                pass
            past_noticed = prnt_noticed 

def measureTemp():
    global hmn_temp
    global hmn_state
    while True:
        time.sleep(0.1)
        lhmn_temp = sensor.get_object_1()
        if lhmn_temp>10:
            hmn_temp = lhmn_temp
        elif (hmn_state == 2) or (hmn_state == 3):
            hmn_temp = 0
        #print(lhmn_temp)

global hmn_dist
global hmn_state
global door_state
global f_path
global mask_state
global imgsaved
global hmn_temp

hmn_dist = 0
hmn_state  = 1 
door_state = 0
f_path = None
mask_state = -1
imgsaved = 0
hmn_temp = 0

proc1 = Thread(target=human_state_check, args=())
proc2 = Thread(target=measureTemp, args=())
proc3 = Thread(target=control_door, args=())
proc4 = Thread(target=mask_check, args=())
proc5 = Thread(target=showtouser, args=())
proc1.start()
proc2.start()
proc3.start()
proc4.start()
proc5.start()