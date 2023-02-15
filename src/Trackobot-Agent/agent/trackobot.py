import cv2
import json
import sys

import numpy as np
import seaborn as sns

from pyzbar.pyzbar import decode
from random import randint
from .utilities import TObject,createTrackerByName
from .utilities import Constants

class Trackobot:
    
    def __init__(self, user_conf, constants = Constants(), unique_colors = 400):
        
        self.app_conf = constants.app_conf
        self.user_conf = user_conf
        
        self.trackerType = "CSRT"
        self.tracker = cv2.MultiTracker_create()
        
        self.tracked_barcodes = []
        self.tracked_objects = []
        self.iter = 0
        
        self.capture = cv2.VideoCapture(self.user_conf["source"])
        self.capture.set(cv2.CAP_PROP_FPS, 15)
        self.capture.set(3,self.app_conf["constants"]["video_width"])
        self.capture.set(4,self.app_conf["constants"]["video_height"])
        
        self._colors = []
        self.constants = constants
        self.iterator = 0
    
    @property
    def inventory(self):
        
        response = {}
        for tracked_object in self.tracked_objects:
            self.iterator +=1
            response[tracked_object.id] = tracked_object.JsonConverter()
        return response    
    
    def adjust_names(self):
        
        for tracked_object in self.tracked_objects:
            
            try:
                tracked_object.name = (self.constants.barcode_names)[tracked_object.barcode]
            except:
                # (self.constants.barcode_names)[tracked_object.barcode] = "Unknown " + str(self.iter) 
                continue
                
    
    def getFrame(self):
        _ , frame = self.capture.read()
        cv2.line(frame, tuple(self.user_conf["seperating_line"]["start_point"]) , 
                 tuple(self.user_conf["seperating_line"]["end_point"]), 
                 tuple(self.user_conf["seperating_line"]["color"]), 
                 int(self.user_conf["seperating_line"]["thickness"]))
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

    # def drawBBoxes(self,bboxes):
    #     iter = 0
    #     for newbox in bboxes:
    #         p1 = (int(newbox[0]), int(newbox[1]))
    #         p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            
    #         cv2.rectangle(frame, p1, p2, self._colors[iter], 2, 1)
    #         iter+=1    
    #     print(iter)

