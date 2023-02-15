import paho.mqtt.client as mqtt
import time 
import datetime
import yaml
import requests


def wlan_ip():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wireless' in i: scan=1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()

mqttBroker = wlan_ip()
client = mqtt.Client("Pc")
client.connect(mqttBroker, port=1883)
r = requests.get("http://127.0.0.1:8000/api/workspaces/?uuid=8")
r = r.json()


user_conf = {
        "source": r["data"]["source"],
        "seperating_line" : {
            "start_point" : (r["data"]["ioCrossline"]["x1"],r["data"]["ioCrossline"]["y1"]),
            "end_point" : (r["data"]["ioCrossline"]["x2"],r["data"]["ioCrossline"]["y2"]),
            "color" : (0,0,0),
            "thickness" : 1
        }
    }

endtime = datetime.datetime.now()+datetime.timedelta(seconds=180)
data_out = yaml.safe_dump(user_conf)
while datetime.datetime.now()<=endtime:
    client.publish("Config",data_out)
    print("Just published "+ str(data_out)+" to Topic Config")
    time.sleep(1)