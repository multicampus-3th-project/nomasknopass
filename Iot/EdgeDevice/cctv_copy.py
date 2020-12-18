import cv2
import time
import requests

cap = cv2.VideoCapture(1) # 0번 카메라
# cap = cv2.VideoCapture('http://192.168.25.4:4747/video') # 스마트폰 카메라 촬영
# cap = cv2.VideoCapture('./data/vtest.avi')  # 우헤헤

### 세팅할 경우 #########################
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
#     int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# print('frame_size = ', frame_size)
pst_time = time.time()
count = 0
while True:
    prnt_time = time.time()
    retval, frame = cap.read()
    cv2.imshow('frame', frame)
    if prnt_time - pst_time > 10:
        fname = './image/test'+str(count)+'.jpg'
        cv2.imwrite(fname,frame)
        imgfile = open(fname, 'rb')
        res = requests.post('http://3.35.178.102/cctvprediction/', files={'image':imgfile})
        print("posted img file = " + fname + " and result" + res.text)
        pst_time = prnt_time
        count = count + 1
    key = cv2.waitKey(25)
    if key == 27: brea
    time.sleep(1)
if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()