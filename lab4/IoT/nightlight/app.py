import time
import json
import paho.mqtt.client as mqtt
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

light_sensor = GroveLightSensor(102)
led = GroveLed(103)

id = '<c2d905c9-ef33-4a92-95e2-2105a8e8372d>'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    if payload['led_on']:
        led.on()
    else:
        led.off()


mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command
while True:
    light = light_sensor.light
    telemetry = json.dumps({'light': light})
    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(5)
