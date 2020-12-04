import cv2
import io
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

class PiCam:
    def __init__(self, show=True, framerate=25, width=640, height=480):
        self.size = (width, height)
        self.show = show
        self.framerate = framerate
        # 이하 미리 셋업을 해서 시간을 버는 방식

        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolutioncamera.resolution = self.size
        self.camera.framerate = self.framerate

    def snapshot(self):
        frame = io.BytesIO()
        self.camera.capture(frame, 'jpeg', use_video_port = True)
        frame.seek(0)
        return frame.getvalue()
    

class MJpegStreamCam(PiCam):
    def __init__(self, show= True, framerate=25, width =640, height=480):
        super().__init__(show=show, framerate=framerate, width=width, height= height)

    def __iter__(self): #열거 가능 객체이기 위한 조건 for x in MJpegStreamingCam() :
        frame = io.BytesIO()
        while True:
            self.camera.capture(frame, format='jpeg', use_video_port = True)
            image = frame.getvalue()
            #순회형 리턴
            yield (b'--myboundary\n' #바이너리 타입으로 리턴할 것이므로... --frame 역할
                    b'Content-Type:image/jpeg\n'                        # --content-Type
                    b'Content-Length: ' + f"{len(image)}".encode() + b'\n' # --content-Length
                    b'\n' + image + b'\n')
            frame.seek(0)
            # frame.truncate(0) #기존 내용은 다 버리겠다....