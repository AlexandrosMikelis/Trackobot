import cv2
import numpy as np
from pyzbar.pyzbar import decode
from datetime import datetime

# conf = {
#     "source":0
# }

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

class Trackobot:
    
    def __init__(self,conf):
        self.conf = conf
        self.initial_state = True
        self.ins = 0
        self.outs = 0
        self.all = 0
        
        self.capture = cv2.VideoCapture(self.conf["source"])
        self.capture.set(3,self.conf["constants"]["video_width"])
        self.capture.set(4,self.conf["constants"]["video_height"])

    def connect(self):
        pass
        
    def getFrame(self):
        _ , frame = self.capture.read()
        return frame
    
    def barcodeDetection(self,img,feedback=False):
        success = False
        TObject = {}
        
        for barcode in decode(img):
            TObject["Barcode"] = barcode.data.decode('utf-8')
            TObject["Rect"] = barcode.rect
            
        if TObject :
            success = True
            if not feedback:
                self.all += 1
            
        return success,TObject
    
    def init_tracker(self,bbox):
        self.tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        self.tracker_type = self.tracker_types[7]
        
        if self.tracker_type == 'BOOSTING':
            self.tracker = cv2.TrackerBoosting_create()
        elif self.tracker_type == 'MIL':
            self.tracker = cv2.TrackerMIL_create()
        elif self.tracker_type == 'KCF':
            self.tracker = cv2.TrackerKCF_create()
        elif self.tracker_type == 'TLD':
            self.tracker = cv2.TrackerTLD_create()
        elif self.tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.TrackerMedianFlow_create()
        elif self.tracker_type == 'GOTURN':
            self.tracker = cv2.TrackerGOTURN_create()
        elif self.tracker_type == 'MOSSE':
            self.tracker = cv2.TrackerMOSSE_create()
        elif self.tracker_type == "CSRT":
            self.tracker = cv2.TrackerCSRT_create()
        
        self.bbox = bbox
        self.ok = self.tracker.init(frame, bbox)
        
    def trackBarcode(self,frame):
        self.ok, self.bbox = self.tracker.update(frame)
        # Draw bounding box
        if self.ok:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            print(p1,p2)
            if p2[0] < self.conf["seperating_line"]["start_point"][0] and self.ins < self.all: 
                self.ins += 1
                self.outs = self.all - self.ins
            if p1[0] > self.conf["seperating_line"]["start_point"][0] and self.outs < self.all: 
                self.outs += 1
                self.ins = self.all - self.outs
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            cv2.putText(frame, "IN" + str(self.ins) , (self.conf["seperating_line"]["start_point"][0] - 100,self.conf["seperating_line"]["start_point"][1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, "OUT" + str(self.outs) , (self.conf["seperating_line"]["start_point"][0] + 100,self.conf["seperating_line"]["start_point"][1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        return self.ok, self.bbox
        

if __name__ == "__main__" :
    
    configuration = {
        "source":'http://192.168.1.9:4747/video',
        "seperating_line" : {
            "start_point" : (250,0),
            "end_point" : (250,500),
            "color" : (0,0,0),
            "thickness" : 3
        },
        "constants" : {
            "video_width" : 500,
            "video_height" : 500
        }
    }
    
    start_point = (250,0)
    end_point = (250,500)
    color = (0,0,0)
    thickness = 3
    
    
    success4barcode = False
    initial_stage = True
    flag = False
    Objects = []
    
    Medicinetracker = Trackobot(configuration)
    # result = cv2.VideoWriter('filename.mp4', 
    #                      cv2.VideoWriter_fourcc(*'mp4v'),
    #                      10, (500,500))
    # Medicinetracker.connect()
    while True:
        frame = Medicinetracker.getFrame()
        cv2.line(frame, start_point, end_point, color, thickness)
        if not success4barcode:
            success4barcode,tracked_barcodeObject = Medicinetracker.barcodeDetection(frame)
            if tracked_barcodeObject:
                Objects.append(tracked_barcodeObject)
                Medicinetracker.init_tracker(Objects[0]["Rect"])
                
        if success4barcode:
    
            # Update tracker
            success,trackedObject = Medicinetracker.barcodeDetection(frame,feedback=True)
            if success:
                Medicinetracker.init_tracker(trackedObject["Rect"])
            ok, bbox = Medicinetracker.trackBarcode(frame)
    
            # Display tracker type on frame
            cv2.putText(frame, Medicinetracker.tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
            
        cv2.imshow("Trackobot",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    Medicinetracker.capture.release()
    # result.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()
   
    print("The video was successfully saved")