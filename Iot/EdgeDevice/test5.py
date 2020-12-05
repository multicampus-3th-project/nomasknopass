import io
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (320, 240)
frame = io.BytesIO()
camera.capture(frame,'png')
frame.seek(0)
frame.getvalue()
print(frame)
data = open('temp.png', 'rb')
data1 = open('sample.png', 'rb')
print("data :",data)
print("data1:",data1)
