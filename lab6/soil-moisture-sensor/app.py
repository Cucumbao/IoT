from counterfit_connection import CounterFitConnection
import time
import json
import paho.mqtt.client as mqtt
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
CounterFitConnection.init('127.0.0.1', 5000)
id = 'd29a8262-3afe-4e98-a929-ec3442f87943'
client_name = id + 'soil-moister'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")
mqtt_client.subscribe(server_command_topic)
print("Commands subscribed!")
adc = ADC()
relay = GroveRelay(103)
def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Command received:", payload)

    if payload["relay_on"]:
        print("Turning relay ON")
        relay.on()
    else:
        print("Turning relay OFF")
        relay.off()
mqtt_client.on_message = handle_command
while True:
    soil_moisture = adc.read(102)
    telemetry = json.dumps({'soil_moisture': soil_moisture})
    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(10)

