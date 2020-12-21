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
from matplotlib import pyplot as plt
import pymysql

image_dir = '/home/ubuntu/kf99_images/'
lambda_client = boto3.client('lambda',
                             region_name='ap-northeast-2',
                             aws_access_key_id='',
                             aws_secret_access_key=''
                             )
sns_client = boto3.client('sns',
                          region_name='ap-northeast-2',
                          aws_access_key_id='',
                          aws_secret_access_key=''
                          )
s3_client = boto3.client('s3',
                         region_name='ap-northeast-2',
                         aws_access_key_id='',
                         aws_secret_access_key=''
                         )
rds_host = "kf99database.cu3wxbwt4src.ap-northeast-2.rds.amazonaws.com"
name = "admin"
password = ""
db_name = "kf99"
conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)


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

        # 기존 모델
        # mask_result = predict_one(filename)
        # if mask_result == 4:
        #     return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        # json_response = {"mask": mask_result,
        #                  "temperature": temperature_result}
        # load.LoadConfig.temperature = temperature_result
        # os.remove(image_dir + filename)
        # return JsonResponse(json_response, status=status.HTTP_200_OK)
        #

        # YOLO 모델
        imageSource = image_dir + filename
        mask, nomask, incorrectmask = predict_cctv(imageSource)

        if mask == 0 and nomask == 0 and incorrectmask == 0:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if mask > 0:
            mask_result = 0
        else:
            mask_result = 1

        if nomask > 0:
            mask_result = 1
        if incorrectmask > 0:
            mask_result = 2

        json_response = {"mask": mask_result,
                         "temperature": temperature_result}
        load.PredictDataConfig.temperature = temperature_result
        os.remove(imageSource)
        return JsonResponse(json_response, status=status.HTTP_200_OK)


@api_view(['POST'])
def predict_mask_cctv(request):
    if request.method == 'POST':
        try:
            filename = str(request.FILES['image'])
            handle_uploaded_file(request.FILES['image'], filename)
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    imageSource = image_dir + filename
    mask, nomask, incorrectmask = predict_cctv(imageSource)

    insert_ismask_cctv(mask, nomask, incorrectmask)

    if load.ImageUploadConfig.count == 7:
        load.ImageUploadConfig.count = 1

    s3_client.upload_file(imageSource, 'kf99-cctv-image', 'cctv-image' + str(load.ImageUploadConfig.count) + '.jpg')
    load.ImageUploadConfig.count += 1

    if nomask > 0 or incorrectmask > 0:
        nomask_state = True
    else:
        nomask_state = False
    nomask_state = True
    load.PredictDataConfig.nomask.append(nomask_state)
    filtering_nomask()

    json_response = {"mask": mask,
                     "nomask": nomask,
                     "incorrectmask": incorrectmask,
                     "array" : load.PredictDataConfig.nomask}

    os.remove(image_dir + filename)

    return JsonResponse(json_response, status=status.HTTP_200_OK)


def filtering_nomask():
    if len(load.PredictDataConfig.nomask) is 6:
        isNoti = True
        for state in load.PredictDataConfig.nomask:
            if state is False:
                isNoti = False
        if isNoti is True:
            notificate_nomask()
        else:
            del (load.PredictDataConfig.nomask[0])


def insert_ismask_cctv(mask, nomask, incorrectmask):
    with conn.cursor() as cur:
        cur.execute("set time_zone=\'Asia/Seoul\'")
        cur.execute(
            "insert into cctv_state(mask, nomask, incorrectmask) values(" + str(mask) + "," + str(nomask) + "," + str(
                incorrectmask) + ")")
        conn.commit()
        cur.close()


@api_view(['POST'])
def insert_ispass(request):
    try:
        ispass = request.data['ispass']
    except:
        return HttpResponse(
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        lambda_client.invoke(
            FunctionName='insert_DB',
            InvocationType='Event',
            Payload=json.dumps({"ispass": request.data['ispass'], "temperature": load.PredictDataConfig.temperature})
        )
    except:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    json_response = {"ispass": ispass,
                     "temperature": load.PredictDataConfig.temperature}
    return HttpResponse(json_response, status=status.HTTP_200_OK)


@api_view(['GET'])
def notificate_emergency(request):
    message = {"GCM": "{ \"data\": { \"title\": \"KF99 Gate\",\"message\": \"누군가 비정상적으로 게이트에 접근했습니다. \" } }"}
    try:
        sns_client.publish(
            # TargetArn='arn:aws:sns:ap-northeast-2:952312817883:endpoint/GCM/kf99_admin/161d6f80-a767-3162-b6d9-53f41cf46c9d',
            # TargetArn='arn:aws:sns:ap-northeast-2:952312817883:endpoint/GCM/kf99_admin/07c925ad-eb2f-31b0-90d6-23af17158f01',
            TargetArn='arn:aws:sns:ap-northeast-2:952312817883:endpoint/GCM/kf99_admin/c3478851-49e2-312e-b8c6-157c831f338e',
            MessageStructure='json',
            Message=json.dumps(message))
    except:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return HttpResponse(status=status.HTTP_200_OK)


def handle_uploaded_file(f, filename):
    with open(image_dir + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def notificate_nomask():
    message = {"GCM": "{ \"data\": { \"title\": \"KF99 CCTV\",\"message\": \"마스크를 벗은 사람이 감지되었습니다. \" } }"}
    sns_client.publish(
        # TargetArn='arn:aws:sns:ap-northeast-2:952312817883:endpoint/GCM/kf99_admin/161d6f80-a767-3162-b6d9-53f41cf46c9d',
        # TargetArn='arn:aws:sns:ap-northeast-2:952312817883:endpoint/GCM/kf99_admin/07c925ad-eb2f-31b0-90d6-23af17158f01',
        TargetArn='arn:aws:sns:ap-northeast-2:952312817883:endpoint/GCM/kf99_admin/c3478851-49e2-312e-b8c6-157c831f338e',
        MessageStructure='json',
        Message=json.dumps(message))
    load.PredictDataConfig.nomask = []


# 얼굴만 자르는 함수 코드
def make_crop_img(image_file, detector):
    result = detector.detect_faces(image_file)
    if not result:
        print('No information')
        return []
    else:
        wh = []
        for t, k in enumerate(result):
            wh.append([k['box'][2] * k['box'][3], t])
        max_i = max(wh)[1]
        bounding_box = result[max_i]['box']

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
def predict_one(chunk):
    # image = cv2.imread(image_dir + filename)
    #
    # try:
    #     images = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     image, message = make_crop_img(images, load.LoadConfig.detector)
    #     face_input = cv2.resize(image, dsize=(224, 224))
    #     face_input = preprocess_input(face_input)
    #     face_input = np.expand_dims(face_input, axis=0)
    #     mask1 = load.LoadConfig.model.predict(face_input)
    #     result = np.argmax(mask1)
    #
    #     if result == 0:
    #         return 0
    #
    #     elif result == 1:
    #         if message == 'not_detected_nose':
    #             return 0
    #         else:
    #             return 1
    #
    #     else:
    #         if message == 'not_detected_nose':
    #             return 0
    #         else:
    #             return 2
    #
    #
    # except:
    #     return 4

    cap = chunk
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(100, 3))
    img = cv2.imread(cap)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    load.LoadConfig.net.setInput(blob)
    output_layers_names = load.LoadConfig.net.getUnconnectedOutLayersNames()
    layerOutputs = load.LoadConfig.net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

    return_label = ''

    area = []

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            area.append([w * h, i])
        print(area)
        l = max(area)[1]
        x, y, w, h = boxes[l]
        label = str(load.LoadConfig.classes[class_ids[l]])

        if label == 'MASK':
            label = 0
        elif label == 'NMASK':
            label = 1
        else:
            label = 2

    return label


def predict_cctv(chunk):
    cap = chunk
    font = cv2.FONT_HERSHEY_PLAIN
    img = cv2.imread(cap)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    load.LoadConfig.net.setInput(blob)
    output_layers_names = load.LoadConfig.net.getUnconnectedOutLayersNames()
    layerOutputs = load.LoadConfig.net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

    return_label = ''

    mask_c = 0
    no_mask_c = 0
    inc_mask_c = 0

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(load.LoadConfig.classes[class_ids[i]])
            if label == 'MASK':
                color = (0, 0, 0)
                mask_c += 1
            elif label == 'NMASK':
                color = (0, 0, 255)
                no_mask_c += 1
            else:
                color = (255, 0, 0)
                inc_mask_c += 1

            confidence = str(round(confidences[i], 2))
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            cv2.putText(img, label + ':' + confidence, (x, y), font, 5, color, 5)
            return_label += label
            print(confidence)

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img2)

    return mask_c, no_mask_c, inc_mask_c
