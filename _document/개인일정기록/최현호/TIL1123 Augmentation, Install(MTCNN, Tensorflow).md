# TIL1123

## (1) Image Augmentation

http://blog.naver.com/4u_olion/221437862590

https://github.com/oryondark/hjkim/blob/master/DeepLearning_master/Augmentation_Tutorial/Data%20Augmentation.md

똑같은 사진이어도 영상처리를 통해 좀 더 밝게 변환, 어둡게 변환, 상하좌우로 이동, 이미지 반전, 이미지 뒤집기 등 다양한 방식으로 이미지의 숫자를 증가시켜 학습하면 학습성능이 좋아 질 수 있다.

이처럼 원본 이미지에 인위적인 변화를 준 이미지들로 충분히 학습에 활용될 수 있는 데이터로 만들 수있다.

이를 **Image Augmentation**이라고 한다. (적은 이미지수로 학습할 때)

다만, Overfitting을 고려해야한다. 과거엔 Overfitting을 해결하기 위해서 모델링 수정(Regularization, Normalization)을 활용했었지만 단지 편향 학습 방향을 조금 죽이는 정도였다.

단순히 편향된 학습은 오류를 발생시키지만, 여기서의 목적은 **적당한 힘으로 학습 면적을 아주 조금 골고루 넓히자는 의미**이다. 따라서 고유 정보가 학습될 때, 해당 정보가 매핑된 공간의 영역을 조금 넓히면서 동시에 크게 벗어나지 않도록 학습하게 된다. 



그렇다면 Augmentation이 항상 좋은 결과만 제공할까? **NO**

딥러닝 분석을 하다보면 생각보다 Augmentation의 결과가 매우 큰 효과를 가져오지 못함을 알 수 있다. Augmentation은 기존의 데이터 정보량을 보존한 상태로 노이즈를 주는 방식이다. 즉 원래 가지고 있는 정보량은 변하지 않는다는 것이다. 단지 정보량에 약간의 변화를 주는 것으로, 딥러닝으로 분석된 데이터의 강력하게 표현되는 고유의 특징을 느슨하게 만다는 것이다. 이는 결과적으로 **오버피팅을 막아줄 수 있고 예측 범위를 약간 넓혀줄 수 있다.**

대신 학습에 필요한 시간이 길어지고, 자원의 소모가 더 커질 수 있다. 또한 깨끗하지 못한 데이터가 있을 수 있다.

이 기술의 가장 큰 핵심은 **Scaling**과 **Rotation**에 있다. 이 두 Method는 솔직히 말하면 극단적으로 변형을 진행하게되면 위험하기 때문에 적절하고 적게 조정해야만 한다.

Rotation : 90도는 Flip에 지나지 않음. 일반적으로 20도 or 30도

Scaling : 50%의 비율로 진행한다고했을떄는 특수한 케이스가 아니라면 이것은 이미 특정 개체로 분류할 수 있는 특징이 담겨진 영역을 한참 초과해버리는 역효과가 나타날 수 있다.  일반적으로 10, 20, 30의 비율내에서 사용



더 다양한 Augmentation 데이터를 만들어 두고, 어떤 것이 더 신속하고 좋은 결과를 가져오는지 평가해야만 한다.

Augmentation의 Method로는 Resize, Scale, Flip, Translate, Rotate, add a noise의 6개 작업이 존재한다. 데이터가 많다고해서 좋은 것은 아니다. 이를 잘 활용하면 Convergence하여 1개의 데이터로 6개가 아닌 2~3개의 데이터로만 증식할 수 있다.



## (2) Image Cropping

아나콘다로 Tensorflow 설치하기(가상환경에 설치) https://bradbury.tistory.com/67

```bash
$ conda activate pydatavenv
$ conda upgrade pip # pip 패키지 최신버전 업그레이드

$ pip install tensorflow --user
$ pip3 install -U pip --user tensorflow # 오류시 이렇게 tensorflow 설치

$ pip install mtcnn
```



#### 다음과 같은 오류발생시

- ImportError: DLL load failed while importing _pywrap_tensorflow_internal: 지정된 모듈을 찾을 수 없습니다.

- Failed to load the native TensorFlow runtime.



#### 해결방안 

- https://needneo.tistory.com/47

- vc_redist.x64.exe 파일(Visual Studio의 파일)을 다운로드 받고 설치 한 후 재부팅 (https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)



## (3) 잘못 분류된 마스크착용 이미지를 정제하는 아이디어

Opencv와 dlib, mtcnn 라이브러리를 이용해서 이미지에서 얼굴의 랜드마크인 코와 입의 좌표값을 가져올 수 있으면 마스크를 제대로 쓰지 못한 이미지로 분류한다.(마스크 미착용 폴더로 이동 및 저장)

https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

```bash
$ conda activate pydatavenv
$ pip install dlib # 에러 날 것이다

$ conda install -c conda-forge dlib # 해결
```



#### MTCNN 문제점

마스크를 쓰고 있어도 코의 좌표를 찾는 성능이 좋은? 예상하지 못한 문제가 있었다.

dlib도 마찬가지로 마스크를 쓰고있어도 코와 입의 좌표를 찾을 것인가?



## 회의

#### AI

예상되는 문제

- 턱이 보이는 잘못 쓴 이미지(합성이미지)인데 마스크를 썻다고 인식

- 인터넷에서 가져온 기존의 모델로는 검은색, 초록색 마스크를 쓴 사람들에 대한 마스크 인식이 부정확한 것 같다 --> 훈련데이터 수가 적었고 색깔에 대한 가중치를 제거하기 위해 흑백스케일링이 필요할 것 같다.
- 다양한 마스크 크기, 색깔이 있는 실제 착용 마스크 데이터 셋을 준비해서 Cropping(크로핑) & Gray-scaling(흑백처리)



- Size Issue : 사이즈에 따라서 모델의 정확성이 달라진다기보다 연산 속도에서 차이가 날뿐이다. 또는 작은 사이즈를 모델학습을 위해 resize할 때 화질이 깨져서 좋은품질의 데이터로 학습시키는 것이 아닌 단점이 있을 수는 있다.