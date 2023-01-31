import cv2
import json
import sys

import numpy as np
import seaborn as sns

from pyzbar.pyzbar import decode
from random import randint
from utilities import TObject,createTrackerByName
from utilities import Constants

class Trackobot:
    
    def __init__(self, app_conf, user_conf, constants = Constants(), unique_colors = 400):
        
        self.app_conf = app_conf
        self.user_conf = user_conf
        
        self.trackerType = "CSRT"
        self.tracker = cv2.MultiTracker_create()
        
        self.tracked_barcodes = []
        self.tracked_objects = []
        self.iter = 0
        
        self.capture = cv2.VideoCapture(self.user_conf["source"])
        self.capture.set(3,self.app_conf["constants"]["video_width"])
        self.capture.set(4,self.app_conf["constants"]["video_height"])
        
        self._colors = []
        self.constants = constants
    
    @property
    def inventory(self):
        response = ""
        for tracked_object in self.tracked_objects:
            response = response + str(tracked_object) + "\n"
        return response    
    
    def adjust_names(self):
        
        for tracked_object in self.tracked_objects:
            tracked_object.name = (self.constants.barcode_names)[tracked_object.barcode]
    
    def getFrame(self):
        _ , frame = self.capture.read()
        cv2.line(frame, self.user_conf["seperating_line"]["start_point"] , 
                 self.user_conf["seperating_line"]["end_point"], 
                 self.user_conf["seperating_line"]["color"], 
                 self.user_conf["seperating_line"]["thickness"])
        return frame

    def barcodeDetector(self,image,feedback=False):
        success = False
        iter = 0
        tobjects = []
        for barcode in decode(image):
            tobjects.append(TObject(iter,barcode.data.decode('utf-8'),barcode.rect))
            iter+=1
        if len(tobjects) > 0 :
            success = True
        
        return success, tobjects
    
    def tracker_init(self, frame, detected_barcodes):
        
        if len(detected_barcodes) == len(self.tracked_barcodes):
            return 1
            
        for tobject in detected_barcodes:
            if tobject.barcode not in self.tracked_barcodes:
                self.tracker.add(createTrackerByName(self.trackerType), frame, tobject.rect)
                self.tracked_barcodes.append(tobject.barcode)
                self._colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))

    
    def tracker_feedback(self, frame, detected_barcodes):
        try:
            bboxes = [ tobject.rect for tobject in detected_barcodes ]
            self.tracker = cv2.MultiTracker_create()
            for bbox in bboxes:
                self.tracker.add(createTrackerByName(self.trackerType), frame, bbox)
            
        except:
            return False
            
    
    def trackBarcodes(self,frame):
        
        success, bboxes = self.tracker.update(frame)
        
        tracked_objects = []
        iter = 0
        
        if success :
            
            # self.drawBBoxes(bboxes)
            
            for barcode,bbox in zip(self.tracked_barcodes,bboxes):
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                if p2[0] <= self.user_conf["seperating_line"]["start_point"][0]:
                    tracked_objects.append(TObject(iter, barcode, bbox, state="IN"))
                if p1[0] > self.user_conf["seperating_line"]["start_point"][0]:
                    tracked_objects.append(TObject(iter, barcode, bbox, state="OUT"))        
                
                cv2.rectangle(frame, p1, p2, self._colors[iter], 2, 1)
                iter+=1 
            self.tracked_objects = tracked_objects
        else:
            
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        
        return success, self.tracked_objects

    def drawBBoxes(self,bboxes):
        iter = 0
        for newbox in bboxes:
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            
            cv2.rectangle(frame, p1, p2, self._colors[iter], 2, 1)
            iter+=1    
        print(iter)

if __name__ == "__main__" :
    
    constants = Constants()
    
    user_conf = {
        "source":'http://192.168.1.2:4747/video',
        "seperating_line" : {
            "start_point" : (250,0),
            "end_point" : (250,500),
            "color" : (0,0,0),
            "thickness" : 1
        }
    }
    
    # user_conf = json.loads(sys.argv[1])
    # user_conf["seperating_line"]["start_point"] = tuple(user_conf["seperating_line"]["start_point"])
    # user_conf["seperating_line"]["end_point"] = tuple(user_conf["seperating_line"]["end_point"])
    # user_conf["seperating_line"]["color"] = tuple(user_conf["seperating_line"]["color"])
    
    app_conf = constants.app_conf
    tracko = Trackobot(app_conf=app_conf, user_conf=user_conf)
    
    barcode_flag = False
    track_flag = False
    res = 0
    succ = True
    
    ins = 0
    outs = 0
    
    while True:
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
    print(tracko.inventory)
    
            
        
        