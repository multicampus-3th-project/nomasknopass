from time import sleep
import time
from picamera import PiCamera
from datetime import datetime
import os
import requests

url = "http://localhost:8000/getimage/"
path_img = "./imagedata/"

# 사진 촬영
camera = PiCamera(resolution=(1280,768), framerate=30)
os.chdir("./imagedata/")

camera.iso = 100
sleep(2)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

fname = datetime.now().strftime("%Y%m%d%H%M")
# print(fname)
camera.capture_sequence([fname+'image%03d.jpg' % i for i in range(3)])




# 사진 전송
with open(path_img, 'rb') as img:
    name_img = os.path.basename(path_img)
    files = {'image':(name_img, img, 'multipart/form-data',{'Expires': '0'})} 
    with requests.Session() as s:
    #requests.post(url, file=image)
    # BytesIO 사용해서 사진 담아 post로 전송
        r = s.post(url, files=files) #
        print(r.status_code)