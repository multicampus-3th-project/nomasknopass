# TIL1124

### 김정현 강사님 멘토링

- 이미지 전처리 등 기술적인 파트 이외에도 포트폴리오에 들어가서 프로젝트 수행 배경 및 시나리오를 강조해줄 수 있는 분석 및 시각화가 들어갈 수도 있다. (어떤 분석을 진행해보니 미래에는 이러이러할 것이다. 따라서 우리 프로젝트의 서비스가 필요하다)
- Tensorflow, Scikit-Learn 등 기본 API 활용할 수 있다 (음성->텍스트로 변환하는 기본 API 등)
  - 많은 부분을 모두 처리해주는 API는 사용을 지양
- 남자 여자 판독모델 : 이미지 수집부터 전처리, 모델링 학습까지 기술 구현의 플로우 참고
  - https://crystalcube.co.kr/192

- 지혜 : 워드클라우드는 왜 우리가 이런 주제를 선정했는지 분석적으로 보여줄려고 진행해보는중..
  '사무직 직업병'을 키워드로 검색해봤을때 특정 oo 단어가 자주 등장하더라. 그래서 우리 서비스가 필요하다.



### 먼저 수작업으로 마스크 착용이미지를 폴더 라벨링하여 1000장의 학습용(Train) 데이터셋 준비

- 이미 크로핑된 사진들이 많지만 추후에 받는 이미지들은 전처리할 때 크로핑과 흑백처리할 수 있을 것



### ImageGenerator from Keras

- 총 2000장(마스크 쓴거 1000장, 안쓴거 1000장)의 raw 이미지 데이터에서  **AI 모델에 학습시킬 때 오버피팅 안되게 Augmentation** 작업을 해줄 필요가 있다. 

- 예를들어 Resizing, Scaling, Translation, Rotation, Flipping, Adding a noise 등 1장의 원본이미지의 데이터에서 약간의 변형을 준 이미지데이터를 생성하여 오버피팅을 방지하고 유연하게 학습시킬 수 있도록 이미지 전처리를 할 수 있다.

  https://github.com/oryondark/hjkim/blob/master/DeepLearning_master/Augmentation_Tutorial/Data%20Augmentation.md