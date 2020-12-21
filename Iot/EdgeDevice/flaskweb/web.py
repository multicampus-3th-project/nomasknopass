# import required modules
from flask import Flask, render_template, Response, jsonify
import numpy as np
import socket, io, time, cv2, os, requests, pigpio, spidev, csv
from gpiozero import Button, DistanceSensor
from datetime import datetime
from signal import pause
from threading import Thread
from multiprocessing import Process
from pydub.playback import play
from pydub import AudioSegment
import pygame


from smbus2 import SMBus
from mlx90614 import MLX90614

# 플라스크 코딩 시작
app = Flask(__name__) 

# 이하 미리 셋업을 해서 시간을 버는 방식
cap = cv2.VideoCapture(0) # 0번 카메라
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

####### 서보모터 동작 (pigpio) ########
pi = pigpio.pi()

#적외선 센서를 이용한 ㅎㅎ
READY_ZONE = 0.35
CHECK_ZONE  = 0.45 #voltage 기준
PASS_ZONE   = 1.2
RETURN_ZONE = 0.25

##적외선센서를 이용한 거리를 측정해봅시다
spi = spidev.SpiDev()
spi.open(0,0) # (버스, 디바이스)
spi.mode = 3
spi.max_speed_hz = 1000000

####MLX90614#####
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)


random_decimal = np.random.rand()

@app.route('/update_decimal', methods = ['POST'])
def updatedecimal():
    global sound_state
    infolog = ''
    if(sound_state == 1):
        infolog = '마스크 확인'
    elif(sound_state == 2):
        infolog = '안녕히 가세요'
    elif(sound_state == 3):
        infolog = '마스크 미착용'
    elif(sound_state == 4):
        infolog = '마스크 오착용'
    elif(sound_state == 5):
        infolog = '발열 확인'
    else:
        pass
    return jsonify('', render_template('random_decimal_model.html', x = infolog))

@app.route('/') 
def index():
   """Video streaming .""" 
   return render_template('index.html', x=0)

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
        if (prnt_time - past_time>1) and hmn_state == 1:
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

def mask_check(): #클라우드와 신호 주고 받기.
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
        lhmn_temp = hmn_temp
        if prnt_time-past_time > 0.5 and (limgsaved == 1) and (lhmn_temp>30): #간격을 0.5로 둠
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
                    print("모델 판단실패, 수신 코드", res.status_code)
            except:
                print("open error occured! filenotError but continue")
            # if   mask_state == 0:# 0 쓴거
            #     print("yMasked", mask_state)
            # elif mask_state == 1:# 1 안쓴거
            #     print("nMasked", mask_state)
            # elif mask_state == 2:# 2 잘못쓴거
            #     print("wMasked", mask_state)
            # elif mask_state == 4:# 4 감지 못한거
            #     print("maskNotFound", mask_state)
            # else:
            #     pass

            #초기화하기
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
    voltage = []
    newList = []
    while True:
        adc = analog_read(0)
        prnt_hmn_dist = adc*3.3/1023 #voltage type
        voltage.append(prnt_hmn_dist)
        #print(prnt_hmn_dist)
        if len(voltage)>9:
            del voltage[0]
            newList = [x for x in voltage if(x>0.35 and x<0.50)]
            if (len(newList)>6) and (hmn_state != 1):
                print("human approached")
                wrongman = 0
                hmn_state =  1
                mask_state = -1
            
        #if len(voltage1)>200:
            #f = open("voltage.csv","w")
            #writer = csv.writer(f)
            #writer.writerow(voltage1)
            #print("```````````````````````````````job done`````````````````````````````````````")
            #break
        #elif past_hmn_dist < CHECK_ZONE and prnt_hmn_dist > CHECK_ZONE and prnt_hmn_dist < PASS_ZONE and hmn_state == 5:
            #print("human approached")
            #wrongman = 0
            #hmn_state =  1
            #mask_state = -1


        if past_hmn_dist < PASS_ZONE and prnt_hmn_dist > PASS_ZONE and hmn_state == 1:
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
        if hmn_state == 1:
            time.sleep(0.10)
            #print(prnt_hmn_dist)
        else:
            time.sleep(0.10)
            #print(prnt_hmn_dist)
        

# sudo pigpiod
def checkingprocess(): #받은 신호와 사람 위치에 따라서 문을 열고 닫는 곳+사람에게 안내하는 곳..
    print("begin control_door")
    global hmn_state
    global mask_state
    global sound_state
    global wrongman
    global hmn_temp
    global door_state
    past_noticed = time.time()
    past_warned = time.time()
    door_state = 0
    pst_door_state = 0
    is_judged = 0
    while True:
        prnt_noticed = time.time()
        prnt_warned = time.time()
        if (prnt_noticed-past_noticed)>0.5: #0.5초간격 실행슨
            lhmn_temp = hmn_temp
            # print(lhmn_temp)
            # print(sound_state)
            if (door_state == 0) and (hmn_state == 1) and (mask_state == 0) and (is_judged == 0) and lhmn_temp < 38 : # 사람이 포토존에 있고, 마스크를 썼을 경우 door_state = 1
                door_state = 1
                is_judged = 1
                sound_state = 1
                print("you can pass")
            elif (door_state == 0) and (hmn_state == 1) and (mask_state == 1) and (prnt_warned-past_warned)>3 and lhmn_temp < 38: #사람이 포토존에 있고, 마스크를 안썼을 경우
                sound_state = 3
                print("you should wear mask")
                past_warned = prnt_warned
            elif (door_state == 0) and (hmn_state == 1) and (mask_state == 2) and (prnt_warned-past_warned)>3 and lhmn_temp < 38: #사람이 포토존에 있고, 마스크를 잘못 썼을 경우
                sound_state = 4
                print("you should wear mask correctly")
                past_warned = prnt_warned
            elif (door_state == 0) and (hmn_state == 1) and (prnt_warned-past_warned)>3 and lhmn_temp > 40: #고열 환자일 경우
                sound_state = 5
                print("you have a fever {0:.1f}".format(lhmn_temp))
                past_warned = prnt_warned
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
            # print(door_state, hmn_state, mask_state)
            
            # if (pst_door_state == 0) and (door_state == 1):
            #     for step in range (100):
            #         pi.set_servo_pulsewidth(25, 1400-8*step)
            #         time.sleep(0.01)
            #     pst_door_state = door_state
            # elif(pst_door_state == 1) and (door_state == 0): #door_state == 0
            #     for step in range (100):
            #         pi.set_servo_pulsewidth(25, 600+8*step)
            #         time.sleep(0.01)
            #     pst_door_state = door_state
            # else:
            #     pass
            # past_noticed = prnt_noticed

def control_door():
    global door_state
    pst_door_state = 0
    past_time = time.time()
    while True:
        prnt_time = time.time()
        prnt_door_state = door_state
        if(prnt_time-past_time)>0.5:
            # print(prnt_door_state)

            #### door open ####
            if (pst_door_state == 0) and (prnt_door_state == 1):
                for step in range (9):
                    pi.set_servo_pulsewidth(25, 1400-100*step)
                    time.sleep(0.05)
                pst_door_state = prnt_door_state

            #### door close ####
            elif(pst_door_state == 1) and (prnt_door_state == 0): #door_state == 0
                for step in range (18):
                    pi.set_servo_pulsewidth(25, 500+50*step)
                    time.sleep(0.05)
                pst_door_state = prnt_door_state
            else:
                pass
            past_time = prnt_time

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

def playSound():
    global sound_state
    pygame.mixer.init()
    is_said = 0
    pst_sound_state = 0
    while True:
        time.sleep(0.2)
        if(sound_state == 1):
            #play(AudioSegment.from_mp3("./sound/normal.mp3"))
            pygame.mixer.music.load("./sound/normal.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        elif(sound_state == 2):
            #play(AudioSegment.from_mp3("./sound/passed.mp3"))
            pygame.mixer.music.load("./sound/passed.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        elif(sound_state == 3):
            #play(AudioSegment.from_mp3("./sound/nomask.mp3"))
            pygame.mixer.music.load("./sound/nomask.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        elif(sound_state == 4):
            # play(AudioSegment.from_mp3("./sound/wrong.mp3"))
            pygame.mixer.music.load("./sound/wrong.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        elif(sound_state == 5):
            # play(AudioSegment.from_mp3("./sound/hightemp.mp3"))
            pygame.mixer.music.load("./sound/hightemp.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
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
global door_state

door_state = 0
hmn_dist = 0
hmn_state  = 1 
f_path = None
mask_state = -1
imgsaved = 0
hmn_temp = 0
wrongman = -1
sound_state = -1
pi.set_servo_pulsewidth(25, 1400)

if __name__ =='__main__':
    thread1 = Thread(target=human_state_check, args=())
    thread4 = Thread(target=measureTemp, args=())
    thread2 = Thread(target=control_door, args=())
    thread3 = Thread(target=mask_check, args=())
    thread5 = Thread(target=playSound, args=())
    thread6 = Thread(target=checkingprocess, args=())

    thread1.start()
    thread4.start()
    thread2.start()
    thread3.start()
    thread5.start()
    thread6.start()
    app.run(host='0.0.0.0', debug=False, threaded=True)
