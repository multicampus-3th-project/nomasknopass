import cv2

cap = cv2.VideoCapture(0) # 0번 카메라
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)




while True:
    _, frame = retval, frame = cap.read()
    cv2.imshow('frame', frame)