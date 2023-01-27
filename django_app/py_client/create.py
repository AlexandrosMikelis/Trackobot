import paho.mqtt.client as mqtt
import time
import json
import requests
endpoint = "http://127.0.0.1:8000/api/products/" 

def on_message(cient,userdata,message):
    m_decode = message.payload.decode("utf-8","ignore")
    m_in = json.loads(m_decode)
    print("Received message: ", str(m_in))
    get_response = requests.post(endpoint, json=m_in) 
    print(get_response.json())



mqttBroker = "192.168.1.4"
client = mqtt.Client("PC")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("Object")
client.on_message = on_message
time.sleep(180)
client.loop_stop()

    