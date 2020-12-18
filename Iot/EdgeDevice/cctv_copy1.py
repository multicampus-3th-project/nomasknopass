import cv2
import numpy as np
import sys
#import time

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
fps = cap.get(cv2.CAP_PROP_FPS)
print("Frames per second using video.get(cv2.CAP_PROP_FPS): {0}".format(fps))


while True:

    ret, image = cap.read()
    image = cv2.GaussianBlur(image,(5,5), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow('Image', image)
 
    if cv2.waitKey(30) > 0:
        break

cv2.destroyAllWindows()