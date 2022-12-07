import cv2
from pyzbar.pyzbar import decode

class TrackoBot:
    
    barcodes = []
    barcodes_bboxes = {}
    
    def __init__(self,config):
        self.config = config
    
    def camera_conn(self):
        try:
            self.capture = cv2.VideoCapture(self.config["VIDEO_CAPTURE_SOURCE"])
            self.capture.set(self.config["FRAME_WIDTH_ID"],self.config["FRAME_WIDTH"])
            self.capture.set(self.config["FRAME_HEIGHT_ID"],self.config["FRAME_HEIGHT"])
            print("Camera Connection - Successful")
        except:
            print("Camera Connection - Failed ==> Please check configuration")
    
    def read_camera(self):
        success, img = self.capture.read()
        return success,img
    
    def barcode_detector(self,image):
        
        curr_barcodes = []
        
        for barcode in decode(image):
            if barcode.data.decode('utf-8'):
                curr_barcodes.append(barcode)
        
        # serial_number = barcode.data.decode('utf-8')
        # rectangle = barcode.rect
        if curr_barcodes:
            self.barcodes = curr_barcodes
        for barcode in curr_barcodes:
            self.barcodes_bboxes[barcode.data.decode('utf-8')] = barcode.rect
    
    def barcode_tracker(self):
        
        success, frame = self.capture.read()
        
        while not self.barcodes:
            self.barcode_detector(frame)
        
        # Specify the tracker type
        trackerType = "CSRT"
        
        # Create MultiTracker object
        multiTracker = cv2.MultiTracker_create()
        
        # Initialize MultiTracker
        for bbox in self.barcodes_bboxes.values:
            multiTracker.add(cv2.TrackerCSRT_create(), frame, bbox)
            
        while self.capture.isOpened():
            success, frame = self.capture.read()
            
            if not success:
                break
            
            # get updated location of objects in subsequent frames
            success, boxes = multiTracker.update(frame)
            
            # draw tracked objects
            for i, newbox in enumerate(boxes):
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, 2, 1)
            
            # show frame
            cv2.imshow('MultiTracker', frame)
            
            # quit on ESC button
            if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
                break