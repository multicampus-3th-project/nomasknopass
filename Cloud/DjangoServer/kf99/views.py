import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import numpy as np
import cv2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from . import load
import boto3
import os

image_dir = '/home/ubuntu/kf99_images/'
lambda_client = boto3.client('lambda',
                             region_name='ap-northeast-2',
                             aws_access_key_id='AKIA53OSENDN4VXRF6JE',
                             aws_secret_access_key='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'
                             )


@api_view(['GET', 'POST'])
def mask(request):
    if request.method == 'GET':
        return HttpResponse("웹페이지 확인용")

    elif request.method == 'POST':
        # file = request.FILES['file']
        filename = str(request.FILES['file'])
        print(filename)
        # image_file = request.FILES['file']
        handle_uploaded_file(request.FILES['file'], filename)
        result = predict_one(filename)
        json_response = {"result": result}

        response = lambda_client.invoke(
            FunctionName='insert_DB',
            InvocationType='Event',
            Payload=json.dumps({"ispass": "0", "temperature": "36.5"})
        )
        print(str(response))

        os.remove(image_dir + filename)

        return JsonResponse(json_response)


def handle_uploaded_file(f, filename):
    with open(image_dir + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# 얼굴만 자르는 함수 코드
def make_crop_img(image_file, detector):
    result = detector.detect_faces(image_file)
    if not result:
        print('No information')
        return []
    else:
        bounding_box = result[0]['box']

        for a in range(4):
            if bounding_box[a] < 0:
                bounding_box[a] = 0

        resizeImageNDArray = image_file.copy()
        resizeImageNDArray = image_file[bounding_box[1]:bounding_box[1] + bounding_box[3],
                             bounding_box[0]:bounding_box[0] + bounding_box[2]]

        nose = load.LoadConfig.nose_cascade.detectMultiScale(resizeImageNDArray)

        if type(nose) == type(np.array([])):
            nd = 'detected_nose'  # 코 검출 : 마스크 불량착용

        else:
            nd = 'not_detected_nose'  # 코 미검출 : 코스크는 아님

        return resizeImageNDArray, nd


# 1장만 할 경우
def predict_one(filename):
    image = cv2.imread(image_dir + filename)

    try:
        images = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image, message = make_crop_img(images, load.LoadConfig.detector)
        face_input = cv2.resize(image, dsize=(224, 224))
        face_input = preprocess_input(face_input)
        face_input = np.expand_dims(face_input, axis=0)
        mask1 = load.LoadConfig.model.predict(face_input)
        result = np.argmax(mask1)

        if result == 0:
            return "mask"

        elif result == 1:
            if message == 'not_detected_nose':
                return "mask"
            else:
                return "no mask"

        else:
            if message == 'not_detected_nose':
                return "mask"
            else:
                return "incorrect mask"


    except:
        return "error"


# 폴더내에 있는 여러장
def predict_many():
    path = glob.glob('/home/lab07/testset/test/*.jpg')

    for t, i in enumerate(path):
        try:
            images = cv2.cvtColor(cv2.imread(i), cv2.COLOR_BGR2RGB)
            image, message = make_crop_img(images, load.LoadConfig.detector)
            face_input = cv2.resize(image, dsize=(224, 224))
            face_input = preprocess_input(face_input)
            face_input = np.expand_dims(face_input, axis=0)
            mask1 = load.LoadConfig.model.predict(face_input)
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
