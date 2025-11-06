from counterfit_connection import CounterFitConnection
import json
import paho.mqtt.client as mqtt
import time
from counterfit_shims_seeed_python_dht import DHT

CounterFitConnection.init('127.0.0.1', 5000)
sensor = DHT("11", 102)

id = '<67161756-5bb3-4956-8b5a-69662237a477>'
client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

while True:
    _, temp = sensor.read()
    telemetry = json.dumps({'temperature': temp})
    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(10)
