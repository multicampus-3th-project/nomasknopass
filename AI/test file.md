test file

```python
import tensorflow as tf
import scipy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.applications import ResNet152V2, ResNet50V2
from tensorflow.keras.applications import DenseNet201, DenseNet121, DenseNet169
from tensorflow.keras.callbacks import ModelCheckpoint



print(tf.__version__)
# 사용할 데이터 부터 준비
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

train_dir1 = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Train/WithoutMask'
train_dir2 = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Train/WithMask'
val_dir1 = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Validation/WithMask'
val_dir2 = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Validation/WithoutMask'

print(len(os.listdir(train_dir1))+len(os.listdir(train_dir2)))
print(len(os.listdir(val_dir1))+len(os.listdir(val_dir2)))


train_dir = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Train'
val_dir = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Validation'



#imageDataGenerator

# train : 14074

train_datagen = ImageDataGenerator(rescale=1/255,
                                   rotation_range=10,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   vertical_flip=True)

validation_datagen = ImageDataGenerator(rescale=1/255)

# train data를 가져오면 => x_data (독립변수, 픽셀데이터), t_data (종속변수, label)
train_generator = train_datagen.flow_from_directory(
    train_dir,                      
    classes=['WithoutMask','WithMask'],               
    target_size = (224,224),
    batch_size = 24,           
    class_mode = 'binary',
   
                                                   )
validation_generator = validation_datagen.flow_from_directory(
    val_dir,           
    classes=['WithoutMask','WithMask'],  
    target_size = (224,224),  
    batch_size = 100,           
    class_mode = 'binary',
    
                                                   )

print(len(train_generator))
print(len(validation_generator))

# 사용할 데이터 부터 준비
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

train_dir = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Train'
val_dir = '/content/drive/MyDrive/마스크_인식/Face Mask Dataset/Validation'



#imageDataGenerator

# train : 14074

train_datagen = ImageDataGenerator(rescale=1/255,
                                   rotation_range=10,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   vertical_flip=True)

validation_datagen = ImageDataGenerator(rescale=1/255)

# train data를 가져오면 => x_data (독립변수, 픽셀데이터), t_data (종속변수, label)
train_generator = train_datagen.flow_from_directory(
    train_dir,                      
    classes=['WithoutMask','WithMask'],               
    target_size = (224,224),
    batch_size = 50 ,           
    class_mode = 'binary',
   
                                                   )
validation_generator = validation_datagen.flow_from_directory(
    val_dir,           
    classes=['WithoutMask','WithMask'],  
    target_size = (224,224),  
    batch_size = 40 ,           
    class_mode = 'binary',
    
                                                   )

# # 데이터 준비완료
# # 모델 생성
# ## Pretrained Network

# model_base = DenseNet169(weights='imagenet',
#                              include_top=False,
#                              input_shape=(224,224,3))

# model_base.trainable = False  # Convolution Layer 완전 동결

# model = Sequential()

# model.add(model_base)

# model.add(Flatten(input_shape=(7*7*1280,)))

# model.add(Dense(3600,
#                 activation='relu'))
# model.add(BatchNormalization())

# model.add(Dense(1,
#                 activation='sigmoid'))

# model.summary()

# lr = 2e-6
# ep = 50

# model.compile(optimizer=Adam(learning_rate = lr),
#               loss='binary_crossentropy',
#               metrics=['accuracy'])

# best_weights_file="weights.best.hdf5"
# checkpoint = ModelCheckpoint(best_weights_file, monitor='val_acc', verbose=1, save_best_only=True, mode='max')


# history = model.fit(train_generator,
# #                             callbacks=[checkpoint],
#                               steps_per_epoch=200,
#                               epochs=20,
#                               validation_data=validation_generator,
#                               validation_steps=20,
#                               verbose=1)


# model_base.trainable = False
# fine_tune = 35


# for layer in model_base.layers[-fine_tune:]:
#       layer.trainable = True

# ## learning rate를 줄이는게 일반적(미세조절)        
# model.compile(optimizer=Adam(learning_rate = lr),
#               loss='binary_crossentropy',
#               metrics=['accuracy'])

# ## 재학습 진행
# history = model.fit(train_generator,
#                          callbacks=[checkpoint],
#                          steps_per_epoch=200,
#                          epochs=ep,
#                          validation_data=validation_generator,
#                          validation_steps=20,
#                          verbose=1)

# train_acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']
# train_loss = history.history['loss']
# val_loss = history.history['val_loss']

# plt.plot(train_acc, 'bo', color='r', label='training accuracy')
# plt.plot(val_acc, 'b', color='b', label='validation accuracy')
# plt.title('Training and Validation Accuracy')
# plt.legend()
# plt.show()

# plt.plot(train_loss, 'bo', color='r', label='training loss')
# plt.plot(val_loss, 'b', color='b', label='validation loss')
# plt.title('Training and Validation Loss')
# plt.legend()
# plt.show()


# model.save('./test_cnn_model_v2.h5')
```

