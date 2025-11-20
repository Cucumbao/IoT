'''

Як можна покращити керуванням поливу

Кожна рослина вимагає свій рівень вологості грунту, тобто при реальній
реалізації системи було б добре додати вибір типу рослини та за допомогою нього
керувати обробкою вологості грунту

Час доби теж має значення, найкраще поливати рослини зранку, коли температура повітря
ще не надто висока. Тоді вода встигає добре зволожити грунт.
Тож можна додати часові вікна, коли дозволено полив (наприклад, 6:00–9:00 або 19:00-22:00).

Якщо вологість критично низька — можна дозволити екстрений полив у будь-який час,
але з меншим потоком води.

Температура повітря впливає на ефективність поливу:
у спеку вода швидко випаровується і полив може бути марним,
тому краще відкласти його на ранок або зменшити інтенсивність.
Тож доцільно було б додати датчик температури повітря або використовувати
прогназ погоди. Та додати обробку даних наприклад:

Якщо температура > 30°C → обмежити полив на 50% або перенести на ранок.

Якщо температура < 10°C → обмежити полив, щоб уникнути застою води.
'''
import json
import time
import paho.mqtt.client as mqtt
import threading
id = 'd29a8262-3afe-4e98-a929-ec3442f87943'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'soil-moister_server'
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
mqtt_client.subscribe(client_telemetry_topic)
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    if payload['soil_moisture'] > 537:
        threading.Thread(target=control_relay, args=(client,)).start()
mqtt_client.on_message = handle_telemetry
water_time = 5
wait_time = 5
def send_relay_command(client, state):
    command = {'relay_on': state}
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))
def control_relay(client):
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)
    send_relay_command(client, True)
    time.sleep(water_time)
    send_relay_command(client, False)
    time.sleep(wait_time)
    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)


while True:
    time.sleep(5)

