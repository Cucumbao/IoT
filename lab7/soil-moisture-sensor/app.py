from counterfit_connection import CounterFitConnection
import time
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

CounterFitConnection.init('127.0.0.1', 5000)

connection_string = "HostName=soil-moisture-sensor-anna.azure-devices.net;DeviceId=soil-moisture-sensor-001;SharedAccessKey=k4/hC1ADIte1vde+c/+PnPZcsjHPG/t53U6EU/vxnwc="

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')

adc = ADC()
relay = GroveRelay(103)


def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        print("Turning relay ON")
        relay.on()
    elif request.name == "relay_off":
        print("Turning relay OFF")
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


device_client.on_method_request_received = handle_method_request

while True:
    soil_moisture = adc.read(102)
    telemetry = json.dumps({'soil_moisture': soil_moisture})
    print("Sending telemetry:", telemetry)
    message = Message(telemetry)
    device_client.send_message(message)
    time.sleep(10)
