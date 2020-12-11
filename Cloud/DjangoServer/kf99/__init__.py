import tensorflow as tf
import os

if os.environ.get('RUN_MAIN', None) != 'true':
    default_app_config = 'load.LoadConfig'

gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
    # 특정 GPU에 1GB 메모리만 할당하도록 제한
    try:
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
    except RuntimeError as e:
        # 프로그램 시작시에 가상 장치가 설정되어야만 합니다
        print(e)
