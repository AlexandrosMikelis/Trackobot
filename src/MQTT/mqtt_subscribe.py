import paho.mqtt.client as mqtt
import time
import yaml
import requests

const_message = {}
def on_message(cient,userdata,message):
    global const_message
    m_decode = message.payload.decode("utf-8","ignore")
    m_in = yaml.safe_load(m_decode)
    const_message = m_in
    print("Received message: ", str(m_in))

def wlan_ip():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wireless' in i: scan=1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()


mqttBroker = wlan_ip()
client = mqtt.Client("PC")
client.connect(mqttBroker)


client.loop_start()
client.subscribe("Inventory")
client.on_message = on_message
time.sleep(100)
client.loop_stop()
payload = {}

for object in const_message.keys():
    payload["barcode"] = const_message[object]['barcode']
    payload["name"] = const_message[object]['name']
    payload["quantity"] = 1
    if const_message[object]['state'] == "OUT":
        payload["In"] = False
        payload["Out"] = True
    elif const_message[object]['state'] == "IN":
        payload["In"] = True
        payload["Out"] = False
    else:
        payload["In"] = False
        payload["Out"] = False
        
    r = requests.post("http://127.0.0.1:8000/api/products/", json=payload)
    payload = {}