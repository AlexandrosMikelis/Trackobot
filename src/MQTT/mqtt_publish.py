import paho.mqtt.client as mqtt
import time 
import json

mqttBroker = "192.168.1.4"
client = mqtt.Client("Pi")
client.connect(mqttBroker, port=1883)
object = {
    "barcode": 5000158105805,
    "brand": "Strepfen"
}

data_out = json.dumps(object)
while True:
    client.publish("Object",data_out)
    print("Just published "+ str(data_out)+" to Topic Object")
    time.sleep(1)