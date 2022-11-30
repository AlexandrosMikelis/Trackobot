from pyzbar.pyzbar import decode

import numpy as np

import cv2
import sys

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

VIDEO_CAPTURE_ID = 1 # 0 is for connected webcam / 1 is for droidcam

FRAME_WIDTH_ID = 3
FRAME_WIDTH = 640

FRAME_HEIGHT_ID = 4
FRAME_HEIGHT = 480

def barcodeTracker():
    pass

def barcodeReader():
    pass

def main():
    barcodeDetected = False
    bboxDetected = False
    flag = False
    
    detectedBarcodes = []
    detectedPolygons = []

    cap = cv2.VideoCapture(VIDEO_CAPTURE_ID)
    cap.set(FRAME_WIDTH_ID,FRAME_WIDTH)
    cap.set(FRAME_HEIGHT_ID,FRAME_HEIGHT)

    # Set up tracker.
    # Instead of CSRT, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
             tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
    
    while True:
        success, img = cap.read()
        
        if not success:
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        timer = cv2.getTickCount()
        
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        if flag :
            success, bbox = tracker.update(img)
            
            if success:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(img, p1, p2, (255,0,0), 2, 1)
            else :
                # Tracking failure
                cv2.putText(img, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                
        if bboxDetected and not flag: 
            success = tracker.init(img, bbox)
            flag = True
                    
        # Display tracker type on frame
        cv2.putText(img,"CSRT Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        # Display FPS on frame
        cv2.putText(img, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
        
        cv2.imshow('Result', img)
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            if myData and myData not in detectedBarcodes :
                
                detectedBarcodes.append(myData)
                barcodeDetected = True
                
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                #cv2.polylines(img,[pts],True,(255,0,255),5)
                if not bboxDetected :
                    bbox = barcode.rect
                    bboxDetected = True 
            # pts2 = barcode.rect
            # cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,0,255),2)

    print(detectedBarcodes)

if __name__ == "__main__" :
    main()