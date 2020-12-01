# TIL1130

## (1) Project Issue

- AI와 빅데이터반 모두 우리가 원하는 분류의 데이터셋을 만들기 위해 직접 맨얼굴에 이미지를 합성시키는 방법으로 데이터셋을 만든다.
- AI반은 턱스크와 코스크를 합성하는 방법을 찾아본다.
- Gray-Resized : https://www.kaggle.com/pranavsingaraju/facemask-detection-dataset-20000-images
- Color : https://www.kaggle.com/prasoonkottarathil/face-mask-lite-dataset
- 이 중에서 컬러사진(23GB)은 흑백처리(600MB)된 이미지보다 용량도 크고 리사이징과 흑백처리를 할 예정이므로 Gray-Resized 이미지를 활용한다.
- 빅데이터반은 먼저 흑백처리된 맨 얼굴 이미지 10000장으로 어떻게 분류할 것인지 생각해보고 밸런스있게 분류한다. 
  - 맨얼굴 3333개, 턱스크 3333개, 코스크 3334개로 1:1:1 분류
  - 턱스크 합성은 축소된 마스크로만 합성되어 턱에 걸쳐져있는 자연스러운 모습이 아니다.
- 잘 착용한 마스크 이미지 합성하는 방법을 https://github.com/aqeelanwar/MaskTheFace 에서 참고하여 흑백처리로 분류된 이미지에 실제 합성을 진행한다.



## (2) dilb 패키지 설치

```bash
conda install -c conda-forge dlib
```



## (3) 인스타 이미지 크롤링

- 테스트 셋을 위한 마스크, 턱스크, 코스크 인스타 이미지 크롤링
