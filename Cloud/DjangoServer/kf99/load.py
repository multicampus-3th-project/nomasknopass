from django.apps import AppConfig
from tensorflow.keras.models import load_model
import cv2
from mtcnn import MTCNN


class LoadConfig(AppConfig):
    model = load_model('/home/lab07/Model_predict/test_mask_model_Densenet201_color_3class_1205.h5')
    haarcascade_dir = '/home/lab07/MTCNN HaarCascade'
    nose_cascade = cv2.CascadeClassifier(haarcascade_dir + '/haarcascade_mcs_nose.xml')
    detector = MTCNN()

    net = cv2.dnn.readNet('/home/lab07/darknet/backup/yolov4_custom_last.weights',
                          '/home/lab07/darknet/custom/yolov4_custom.cfg')
    # 파일 주소 확인
    classes = []
    with open("/home/lab07/darknet/custom/custom.name", "r") as f:
        # 파일 주소 확인
        classes = f.read().splitlines()


class PredictDataConfig(AppConfig):
    # Gate 체온 데이터
    temperature = 0
    # CCTV 마스크 미착용자 감지 카운트
    nomask = []


class ImageUploadConfig(AppConfig):
    count = 1
