import requests
import os


# 사진 전송
imgfile = open("sample.png", 'rb')
r = requests.post('http://3.35.94.100:8000/mask/', files = {'sampleimgfromraspberry':imgfile})