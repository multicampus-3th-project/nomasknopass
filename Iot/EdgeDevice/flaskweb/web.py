# import required modules
from flask import Flask, render_template, Response 
import socket 
import io
from gpiozero import Button, DistanceSensor
from datetime import datetime
from signal import pause
import time
from threading import Thread
from multiprocessing import Process
import pigpio
import cv2
import requests
import os
from pydub.playback import play
import spidev
from smbus2 import SMBus
from mlx90614 import MLX90614
from pydub import AudioSegment
from pydub.playback import play

# 안녕 나는 플라스크 용 플라스크라고 한다.
app = Flask(__name__) 

# 이하 미리 셋업을 해서 시간을 버는 방식
cap = cv2.VideoCapture(0) # 0번 카메라
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

####### 서보모터 동작 (pigpio) ########
pi = pigpio.pi()

#적외선 센서를 이용한 ㅎㅎ
READY_ZONE = 0.22
CHECK_ZONE  = 0.38 #voltage 기준
PASS_ZONE   = 1.0
RETURN_ZONE = 0.2

##적외선센서를 이용한 거리를 측정해봅시다
spi = spidev.SpiDev()
spi.open(0,0) # (버스, 디바이스)
spi.mode = 3
spi.max_speed_hz = 1000000

####MLX90614#####
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)


@app.route('/') 
def index(): 
   """Video streaming .""" 
   return render_template('index.html') 
def gen(): 
   """Video streaming generator function."""
   global f_path
   global imgsaved
   past_time = time.time()
   while True: 
        rval, frame = cap.read()
        frame = cv2.flip(frame, 1)
        byteArray = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n')
        ### 2초 간격으로 이미지 파일을 저장 ###
        prnt_time = time.time()
        if (prnt_time - past_time>2) and hmn_state == 1:
            # fname = datetime.now().strftime("%Y%m%d%H%M%S")
            # f_path = "./image/"+fname+".jpg"
            # cv2.imwrite(f_path,frame)
            is_success, f_path = cv2.imencode(".jpg", frame)
            imgsaved = 1
            past_time = prnt_time
            # print("captured!")

@app.route('/video_feed') 
def video_feed(): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

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
        if prnt_time-past_time > 0.5 and (limgsaved == 1) and (lhmn_temp>30): #간격을 1로 둠
            try:
                # imgfile = open(lf_path, 'rb')
                imgfile = io.BytesIO(lf_path)
                res = requests.post('http://3.35.178.102/gateprediction/', files={'image':imgfile}, data={"temperature":lhmn_temp}) #이거슨 그.. 온도도 보낼 때
                # imgfile.close()
                # try:
                #     os.remove(lf_path)
                # except FileNotFoundError:
                #     print("delete error occured! filenotError but continue")
                #     pass
                if res.status_code == 200:
                    mask_state = res.json()['mask']
                else:
                    print("모델 판단실패, 수신 코드",res.status_code)
            except FileNotFoundError:
                print("open error occured! filenotError but continue")
            #     pass
            if   mask_state == 0:# 0 쓴거
                print("yesMasked", mask_state)
            elif mask_state == 1:# 1 안쓴거
                print("noMasked",mask_state)
            elif mask_state == 2:# 2 잘못쓴거
                print("wrongMasked", mask_state)
            elif mask_state == 4:# 4 감지 못한거
                print("maskNotFound", mask_state)
            else:
                pass
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
    global wrongman
    global mask_state
    prnt_hmn_dist = 0
    past_hmn_dist = 0
    while True:
        adc = analog_read(0)
        prnt_hmn_dist = adc*3.3/1023 #voltage type
        # print("Voltage = %.4fV" % (voltage))
        if hmn_state == 1:
            time.sleep(0.05)
        else:
            time.sleep(0.15)
        # print("past:{0:.3f}, prsnt:{1:.3f}".format(past_hmn_dist,prnt_hmn_dist))
        if past_hmn_dist < READY_ZONE and prnt_hmn_dist > READY_ZONE and prnt_hmn_dist < CHECK_ZONE:
            print("ready set")
            hmn_state = 5
        if past_hmn_dist < CHECK_ZONE and prnt_hmn_dist > CHECK_ZONE and prnt_hmn_dist < PASS_ZONE and hmn_state == 5:
            print("human approached")
            wrongman = 0
            hmn_state =  1
            mask_state = -1
        elif past_hmn_dist < PASS_ZONE and prnt_hmn_dist > PASS_ZONE and hmn_state == 1:
            print("human passed")           
            hmn_state = 2
        elif past_hmn_dist > RETURN_ZONE and prnt_hmn_dist < RETURN_ZONE and past_hmn_dist < PASS_ZONE and hmn_state == 1:
            print("human returned")
            hmn_state = 3
            mask_state = -1
            res = requests.post('http://3.35.178.102/visit/',data={"ispass":0})
        else:
            pass
        past_hmn_dist = prnt_hmn_dist
        

# sudo pigpiod
def control_door(): #받은 신호와 사람 위치에 따라서 문을 열고 닫는 곳+사람에게 안내하는 곳..
    print("begin control_door")
    global hmn_state
    global mask_state
    global sound_state
    past_noticed = time.time()
    door_state = 0
    pst_door_state = 0
    is_judged = 0
    global wrongman
    while True:
        prnt_noticed = time.time()
        if (prnt_noticed-past_noticed)>0.5: #0.5초간격 실행슨
            if (door_state == 0) and (hmn_state == 1) and (mask_state == 0) and (is_judged == 0): # 사람이 포토존에 있고, 마스크를 썼을 경우 door_state = 1
                door_state = 1
                is_judged = 1
                sound_state = 1
                print("you can pass")
            elif(door_state == 1) and (hmn_state == 2) and (is_judged == 1): # 멀쩡한 사람이 통과를 했을 경우 door_state  = 0
                door_state = 0
                is_judged = 0
                res = requests.post('http://3.35.178.102/visit/',data={"ispass":1})
                sound_state = 2
                print("door closed")
            elif (door_state == 1) and (hmn_state == 3) and (is_judged == 1): # 멀쩡한 사람이 떠났을 경우 door_state  = 0
                door_state = 0
                is_judged = 0
                print("door closed")
            elif (door_state == 0) and (hmn_state == 2) and mask_state != 0 and (wrongman == 0) and (is_judged == 0):
                print("wrong man passed")
                wrongman = 1
                res = requests.get('http://3.35.178.102/emergency/')
            else:
                pass
            
            if (pst_door_state == 0) and (door_state == 1):
                print("door open")
                for step in range (100):
                    pi.set_servo_pulsewidth(25, 1400-8*step)
                    time.sleep(0.01)
                pst_door_state = door_state
            elif(pst_door_state == 1) and (door_state == 0): #door_state == 0
                for step in range (100):
                    pi.set_servo_pulsewidth(25, 600+8*step)
                    time.sleep(0.01)
                pst_door_state = door_state
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

def pushtoAdmin():
    while True:
        button.wait_for_press()
        print("The button was pressed!")

def playSound():
    global sound_state
    while True:
        time.sleep(0.2)
        if(sound_state == 1):
            play(AudioSegment.from_mp3("./sound/passed.mp3"))
        elif(sound_state == 2):
            play(AudioSegment.from_mp3("./sound/closed.mp3"))
        else:
            pass
        sound_state = 0
        


global hmn_dist
global hmn_state
global f_path
global mask_state
global imgsaved
global hmn_temp
global wrongman
global sound_state


hmn_dist = 0
hmn_state  = 1 
f_path = None
mask_state = -1
imgsaved = 0
hmn_temp = 0
wrongman = -1
sound_state = -1

pi.set_servo_pulsewidth(25, 1400)


proc1 = Thread(target=human_state_check, args=())
# proc2 = Thread(target=measureTemp, args=())
proc3 = Thread(target=control_door, args=())
proc4 = Thread(target=mask_check, args=())
proc6 = Thread(target=pushtoAdmin, args=())
proc7 = Thread(target=playSound, args=())
proc1.start()
# proc2.start()
proc3.start()
proc4.start()
proc6.start()
proc7.start()
app.run(host='0.0.0.0', debug=False, threaded=True)
