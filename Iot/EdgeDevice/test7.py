import requests
import os
import time
from datetime import datetime

# 사진 전송

imgfile = open("./image/20201207152639.jpg", 'rb')
a=time.time()
r = requests.post("http://3.35.178.102:8888/mask/", files = {'file':imgfile})
b= time.time()
print(r.text)

print(b-a)