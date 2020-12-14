import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import numpy as np
import cv2
from rest_framework import status
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
sns_client = boto3.client('sns',
                          region_name='ap-northeast-2',
                          aws_access_key_id='AKIA53OSENDNTMPJOQTE',
                          aws_secret_access_key='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'
                          )


@api_view(['GET', 'POST'])
def predict_mask_gate(request):
    if request.method == 'GET':
        return HttpResponse("웹페이지 확인용", status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            filename = str(request.FILES['image'])
            handle_uploaded_file(request.FILES['image'], filename)
            temperature_result = request.data['temperature']
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        mask_result = predict_one(filename)

        if mask_result == 4:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        json_response = {"mask": mask_result,
                         "temperature": temperature_result}
        load.LoadConfig.temperature = temperature_result
        os.remove(image_dir + filename)
        return JsonResponse(json_response, status=status.HTTP_200_OK)


@api_view(['POST'])
def predict_mask_cctv(request):
    if request.method == 'POST':
        try:
            filename = str(request.FILES['image'])
            handle_uploaded_file(request.FILES['image'], filename)
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    # .....
    os.remove(image_dir + filename)
    # .....


@api_view(['POST'])
def insert_ispass(request):
    try:
        ispass = request.data['ispass']
    except:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    try:
        lambda_client.invoke(
            FunctionName='insert_DB',
            InvocationType='Event',
            Payload=json.dumps({"ispass": request.data['ispass'], "temperature": load.LoadConfig.temperature})
        )
    except:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    json_response = {"ispass": ispass,
                     "temperature": load.LoadConfig.temperature}
    return HttpResponse(json_response, status=status.HTTP_200_OK)


@api_view(['GET'])
def notificate_emergency(request):
    message = {"GCM": "{ \"data\": { \"title\": \"KF99\",\"message\": \"누군가 비정상적으로 게이트에 접근했습니다. \" } }"}
    try:
        sns_client.publish(
            TargetArn='arn:aws:sns:ap-northeast-2:952312817883:endpoint/GCM/kf99_admin/161d6f80-a767-3162-b6d9-53f41cf46c9d',
            MessageStructure='json',
            Message=json.dumps(message))
    except:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return HttpResponse(status=status.HTTP_200_OK)


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
            return 0

        elif result == 1:
            if message == 'not_detected_nose':
                return 0
            else:
                return 1

        else:
            if message == 'not_detected_nose':
                return 0
            else:
                return 2


    except:
        return 4


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
