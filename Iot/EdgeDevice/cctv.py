import time
import picamera
import requests

with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.framerate = 15
    camera.start_preview()
    time.sleep(2)
    count = 1
    while True:
        fname = './image/test'+str(count)+'.jpg'
        camera.capture(fname)
        imgfile = open(fname, 'rb')
        res = requests.post('http://3.35.178.102/cctvprediction/', files={'image':imgfile})
        print("CCTV Result" + res.text)
        count = count + 1
        time.sleep(6)
    camera.stop_preview()