import paho.mqtt.client as mqtt
import time
import json

def on_message(cient,userdata,message):
    m_decode = message.payload.decode("utf-8","ignore")
    m_in = json.loads(m_decode)
    print("Received message: ", str(m_in))

mqttBroker = "192.168.1.4"
client = mqtt.Client("PC")
client.connect(mqttBroker)


client.loop_start()
client.subscribe("Object")
client.on_message = on_message
time.sleep(30)
client.loop_stop()
