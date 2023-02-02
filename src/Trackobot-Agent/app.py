import cv2

from agent import Trackobot

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
    
    user_configuration = {}
    return user_configuration

def mqtt_sendInventory(inventory):
    # Add here the needed code so as to send inventory dictionary to mqtt
    return 

if __name__ == "__main__" :
    
    barcode_flag = False
    track_flag = False
    succ = True
    switch = False
    
    res = 0
    ins = 0
    outs = 0
    
    switch = mqtt_trigger()
    
    user_conf = mqtt_getUserConf()
    
    tracko = Trackobot(user_conf=user_conf)
    
    while switch:
        switch = mqtt_trigger()
        
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
        
        mqtt_sendInventory(tracko.inventory)
        
    print(tracko.inventory)
    
            
        
        