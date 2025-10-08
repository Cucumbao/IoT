import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

light_sensor = GroveLightSensor(102)
led = GroveLed(103)

while True:
    light = light_sensor.light
    if light < 1020:
        led.on()
    else:
        led.off()
    print('Light level:', light)
    time.sleep(1)

