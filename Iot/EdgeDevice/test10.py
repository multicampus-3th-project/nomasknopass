###### AI 모델을 직접 라즈베리 파이에 옮겨 테스트를 시도해봅니다.
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from mtcnn import MTCNN
import warnings

warnings.filterwarnings('ignore')
plt.style.use('dark_background')

# 모델 불러오는 코드
model = load_model('./model/test_mask_model_Densenet201_color_3class_1205.h5')

# 얼굴만 자르는 함수 코드
def make_crop_img(image_file, detector):
    result = detector.detect_faces(image_file)
    if result == []:
        print('No information')
        return []
    else:
        bounding_box = result[0]['box']
        
        for a in range(4):
            if bounding_box[a] < 0:
                bounding_box[a] = 0
                
        resizeImageNDArray = image_file.copy()
        resizeImageNDArray = image_file[bounding_box[1]:bounding_box[1]+bounding_box[3], bounding_box[0]:bounding_box[0]+bounding_box[2]]

        nose = nose_cascade.detectMultiScale(resizeImageNDArray)

        if type(nose) == type(np.array([])):
            nd = 'detected_nose' # 코 검출 : 마스크 불량착용

        else:
            nd = 'not_detected_nose' # 코 미검출 : 코스크는 아님
        
        return resizeImageNDArray, nd
    
haarcascade_dir = './model'
nose_cascade = cv2.CascadeClassifier(haarcascade_dir + '/haarcascade_mcs_nose.xml')
detector = MTCNN()


# 1장만 할 경우 cv2.imread('/home/lab07/test_data_3lass/without_mask/MOXA_1271.jpg'

try:
    images = cv2.cvtColor(cv2.imread('./image/20201207152640.jpg'), cv2.COLOR_BGR2RGB) 
    image, message = make_crop_img(images, detector)
    face_input = cv2.resize(image, dsize=(224, 224))
    face_input = preprocess_input(face_input)
    face_input = np.expand_dims(face_input, axis=0)
    mask1 = model.predict(face_input)
    result = np.argmax(mask1)

    if result == 0:
        print(0)

    elif result == 1:
        if message == 'not_detected_nose':
            print(0)
        else:
            print(1)

    else:
        if message == 'not_detected_nose':
            print(0)
        else:
            print(2)

except:
    print(4)


# # 폴더내에 있는 여러장

# path = glob.glob('/home/lab07/testset/test/*.jpg')

# for t,i in enumerate(path):
#     try:
#         images = cv2.cvtColor(cv2.imread(i), cv2.COLOR_BGR2RGB) 
#         image, message = make_crop_img(images, detector)
#         face_input = cv2.resize(image, dsize=(224, 224))
#         face_input = preprocess_input(face_input)
#         face_input = np.expand_dims(face_input, axis=0)
#         mask1 = model.predict(face_input)
#         result = np.argmax(mask1)

#         if result == 0:
#             print(0)

#         elif result == 1:
#             if message == 'not_detected_nose':
#                 print(0)
#             else:
#                 print(1)

#         else:
#             if message == 'not_detected_nose':
#                 print(0)
#             else:
#                 print(2)

#     except:
#         print(4)