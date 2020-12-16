import spidev, time
def analog_read(channel):
    # 매개변수 (시작비트, 채널, 자릿수 맞춤 위치), 리턴값 : 아날로그 값
    r = spi.xfer2([1, (0x08+channel)<<4, 0])
    adc_out = ((r[1]&0x03)<<8) + r[2] # 수신 데이터 결합
    return adc_out
spi = spidev.SpiDev()
spi.open(0,0) # (버스, 디바이스)
spi.mode = 3
spi.max_speed_hz = 1000000
while True:
    adc = analog_read(0)
    voltage = adc*3.3/1023
    print("ADC = %s(%d) Voltage = %.3fV" % (hex(adc), adc, voltage))
    time.sleep(0.1)