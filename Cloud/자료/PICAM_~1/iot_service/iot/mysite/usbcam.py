import cv2

class USBCam:
    def __init__(self, show = False, framerate = 25, width = 640, height = 480):
        self.size = (width, height)
        self.show = show
        self.framerate = framerate
        # 이하 미리 셋업을 해서 시간을 버는 방식
        self.cap = cv2.VideoCapture(0) # 0번 카메라
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.size[1])

    def snapshot(self):
        retval, frame = self.cap.read() # 프레임 캡처, frame: numpy 배열 opencv 는 bgr
        #retval 성공 여부, frame 은 저장 메모리
        if retval :
            _, jpg = cv2.imencode('.JPEG',frame) # imencode
                                                 # _ 사용하지 않는 관례형 변수
            return jpg.tobytes() #원래는 numpy배열이지만,,, tobytes를 통해 bytes string으로 변환스
    
class MJpegStreamCam(USBCam):
    def __init__(self, show= True, framerate=25, width =640, height=480):
        super().__init__(show=show, framerate=framerate, width=width, height= height)

    def __iter__(self): #열거 가능 객체이기 위한 조건 for x in MJpegStreamingCam() :
        while True:
            retval, frame = self.cap.read()
            _, jpg = cv2.imencode('.JPEG',frame) #--frame으로 둘러쌓인 JPEG data 응답 메세지를 형성하는 역할--
            #순회형 리턴!
            yield(
                b'--myboundary\n' #바이너리 타입으로 리턴할 것이므로... --frame 역할
                b'Content-Type:image/jpeg\n'                        # --content-Type
                b'Content-Length: ' + f"{len(jpg)}".encode() +b'\n' # --content-Length
                b'\n' + jpg.tobytes()+ b'\n'
            )