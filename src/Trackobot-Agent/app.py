import cv2
import paho.mqtt.client as mqtt
import time
import json
import yaml
from agent import Trackobot
import datetime


const_message = {}
def on_message(cient,userdata,message):
    global const_message
    m_decode = message.payload.decode("utf-8","ignore")
    m_in = yaml.safe_load(m_decode)
    const_message = m_in
    print(const_message)
    

def mqtt_start():
    # A function to start the mqtt subscriber
    # return a boolean variable named switch representing if the proccess was successful or not
    return

def mqtt_stop():
    # function to stop mqtt subscriber to receiving
    return

def mqtt_trigger():
    # probably a merged functionality of start and stop function, you will see
    return

def mqtt_post():
    return

def mqtt_get():
    return

def mqtt_getUserConf():
    # Add here the needed code so as to get user configuration dictionary from mqtt
    # Example of USER_CONF variable
    
    # user_conf = {
    #     "source":'http://192.168.1.2:4747/video',
    #     "seperating_line" : {
    #         "start_point" : (250,0),
    #         "end_point" : (250,500),
    #         "color" : (0,0,0),
    #         "thickness" : 1
    #     }
    # }
    
    
    user_configuration={}
    while not user_configuration:
        try:
            
            client.loop_start()
            client.subscribe("Config")
            client.on_message = on_message
            if const_message:
                user_configuration = const_message
                print(user_configuration)
                
                client.loop_stop()
                return user_configuration
            
        except:   
            user_configuration = {
                "source":'http://192.168.1.3:4747/video',
                "seperating_line" : {
                    "start_point" : (250,0),
                    "end_point" : (250,500),
                    "color" : (255,255,0),
                    "thickness" : 1
                }
            }
            return user_configuration

def get_keys(input_dict):
    for key, value in input_dict.items():
        if isinstance(value, dict):
            for subkey in get_keys(value):
                yield key + '/' + subkey
        else:
            yield key



def mqtt_sendInventory(inventory):
    # Add here the needed code so as to send inventory dictionary to mqtt
    return 

def wlan_ip():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wireless' in i: scan=1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()


if __name__ == "__main__" :
    mqttBroker = wlan_ip()
    client = mqtt.Client("Raspberry")
    client.connect(mqttBroker)

    barcode_flag = False
    track_flag = False
    succ = True
    switch = True
    
    res = 0
    ins = 0
    outs = 0
    

    # switch = mqtt_trigger()
    
   
    user_conf = mqtt_getUserConf()
    print(user_conf)
    print(type(user_conf))
    # user_conf = {
    #     "source":'http://192.168.1.4:4747/video',
    #     "seperating_line" : {
    #         "start_point" : (250,0),
    #         "end_point" : (250,500),
    #         "color" : (0,0,0),
    #         "thickness" : 1
    #     }
    # }
    tracko = Trackobot(user_conf=user_conf)
    endtime = datetime.datetime.now()+datetime.timedelta(seconds=15)
    while switch:
        # switch = mqtt_trigger()
       
        frame = tracko.getFrame()
        
        success, detected_barcodes = tracko.barcodeDetector(frame)
        
        if success :
            
            res = tracko.tracker_init(frame, detected_barcodes)
            
        if res == 1 and success :
            success_feedback = tracko.tracker_feedback(frame, detected_barcodes)
            succ, tracked_objects = tracko.trackBarcodes(frame)  
            for tobject in tracked_objects:
                if tobject.state == "OUT":
                    outs +=1
            
            ins = len(tracko.tracked_objects) - outs
               
        cv2.putText(frame, "IN" + str(ins) , (tracko.user_conf["seperating_line"]["start_point"][0] - 100,tracko.user_conf["seperating_line"]["start_point"][1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        cv2.putText(frame, "OUT" + str(outs) , (tracko.user_conf["seperating_line"]["start_point"][0] + 100,tracko.user_conf["seperating_line"]["start_point"][1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        cv2.imshow("Trackobot",frame)
        
        if res == 1 and success :
            ins,outs = 0,0
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        tracko.adjust_names()
        if (tracko.inventory and datetime.datetime.now()>=endtime):
            data_out = yaml.dump(tracko.inventory, default_flow_style=False)
            client.publish("Inventory",data_out)
            print("Just published "+ str(data_out)+" to Topic Inventory")
            endtime = datetime.datetime.now()+datetime.timedelta(seconds=15)
        # mqtt_sendInventory(tracko.inventory)
    
    # tracko.adjust_names()
    
    # print(tracko.inventory)

    # #
    # data_out = string
    # client.publish("Config",data_out)
    # print("Just published "+ str(data_out)+" to Topic Config")
    
            
        
        