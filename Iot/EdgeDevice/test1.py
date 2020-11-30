from gpiozero import DistanceSensor
import cv2
import io
import random
from picamera import PiCamera, PiCameraCircularIO

#기동

global state = -1
sensor = DistanceSensor(23, 24)
PH_ZONE_MIN = 0.2 #사진 촬영시작 zone
PH_ZONE_MAX = 0.6 #사진 촬영종료 zone
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

def human_detected():
    # 이 부분을 어떻게 하느냐에 따라 다양한 방법을 사용할 수 있스다. 
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0 #난수 생성해서 0이면 디텍티드?? 무엇
    # return 0.5 <= 0.2 #20cm 안에 들어오면 True ,,, 근접함
def mask_detected():
    return random.randint(0,10) == 1

def white_rectangle():
    cv2.rectangle(frame, (int(cap_width/4),int(cap_height/6)),(int(cap_width*3/4),int(cap_height*5/6)), (255, 255, 255), 2)

def green_rectangle():
    cv2.rectangle(frame, (int(cap_width/4),int(cap_height/6)),(int(cap_width*3/4),int(cap_height*5/6)), (0, 255, 0), 2)

def yellow_rectangle():
    cv2.rectangle(frame, (int(cap_width/4),int(cap_height/6)),(int(cap_width*3/4),int(cap_height*5/6)), (0, 255, 255), 2)

def human_approached(): #edge trigger
    return False

def face_detected(): #level trigger
    return False

def responsed(): #level trigger
    return False

def human_forcedPassed(): #edge trigger
    return False

def manager_called(): #edge trigger
    return False

def human_passed(): #edge trigger
    return False

def human_returned(): #edge trigger
    return False

def checking_mask():
    return False


#While 문 시작 시점
while True:
    # 초음파센서 주기적으로 획득
    if human_approached(): #사람이 들어오면?(초음파센서)
        print("human approached")
        #카메라 기동
        ret, frame = cap.read()
        if  human_detected():
            yellow_rectangle()
        elif mask_detected():
            green_rectangle()
        else :
            white_rectangle()
        cv2.imshow('video',frame)
        #카메라에 얼굴 들이대달라 권고
        print("please face to the camera")

        while responsed(): #결과(마스크와 얼굴) 감지 하면 다음 단계
                #촬영 on
                print('please wait a sec') #이용자에게 대기 요청
                #클라우드에서 전송값 받을 때까지 while 문 수
        
        #감지가 되면
        state = checking_mask()

        #결단을 내리고
        if (state == 1) :
            print("you can pass!")
            #서보모터 동작
        else :
            print("you cannot pass.")
            #돌아가라는 메시지 표시
            #부저음(static)

    elif human_forcedPassed():
        print('emergency on')
        #아까 저장한 촬영 이미지 관리자에게 송신
        #게이트문 재위치
    
    elif human_passed():
        print('human passed')
        #게이트문 재위치
    
    elif human_returned():
        print('human returned')

    else :
        continue


if manager_called():
    print('manager called')


#초기상황으로 돌아감(While문 종료 시점)
