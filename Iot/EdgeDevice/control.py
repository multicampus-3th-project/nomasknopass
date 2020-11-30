import cv2
from picamera import PiCamera
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(13, 19)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#0.38 초 걸린다.
while True:
    ret, frame = cap.read()
    if False:
        cv2.rectangle(frame, (int(cap_width/4),int(cap_height/6)),(int(cap_width*3/4),int(cap_height*5/6)), (255, 255, 255), 2)
    cv2.imshow('image',frame)
    if (cv2.waitKey(1) == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()