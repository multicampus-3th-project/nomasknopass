#사진을 찍고, 파일을 보내고 응답을 받는다.
import cv2, io, time
from PIL import Image
import requests
import numpy as np

cap = cv2.VideoCapture(0) # 0번 카메라
# cap = cv2.VideoCapture('http://192.168.25.4:4747/video') # 스마트폰 카메라 촬영
# cap = cv2.VideoCapture('./data/vtest.avi')  # 우헤헤

### 세팅할 경우 #########################
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
#     int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# print('frame_size = ', frame_size)

pst_time = time.time()
while True:
    prnt_time = time.time()
    retval, frame = cap.read() # 프레임 캡처
    if not retval: break
    cv2.imshow('frame', frame)

    if prnt_time-pst_time > 3:
        # f_path = './image/test.jpg'
        # cv2.imwrite(f_path,frame)
        # with open(f_path,'rb') as f:
        is_success, buffer = cv2.imencode(".jpg", frame)
        io_buf = io.BytesIO(buffer)
        res = requests.post('http://3.35.178.102/gateprediction/', files={'image':io_buf}, data={"temperature":36.5})
        print(res.text)
        pst_time = prnt_time


    key = cv2.waitKey(25)
    if key == 27: break # ESC키를 누른 경우 루프 탈출
if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()