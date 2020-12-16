from smbus2 import SMBus
from mlx90614 import MLX90614
import time

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

while True:
    time.sleep(2)
    print("Object Temperature : {0:.2f}".format(sensor.get_object_1()))
bus.close()