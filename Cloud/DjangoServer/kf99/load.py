from django.apps import AppConfig
from tensorflow.keras.models import load_model
import cv2
from mtcnn import MTCNN


class LoadConfig(AppConfig):
    model = load_model('/home/lab07/Model_predict/test_mask_model_Densenet201_color_3class_1205.h5')
    haarcascade_dir = '/home/lab07/MTCNN HaarCascade'
    nose_cascade = cv2.CascadeClassifier(haarcascade_dir + '/haarcascade_mcs_nose.xml')
    detector = MTCNN()
    temperature = 0

    def ready(self):
        pass

