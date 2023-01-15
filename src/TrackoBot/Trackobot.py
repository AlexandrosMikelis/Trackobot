import cv2
import numpy as np

from pyzbar.pyzbar import decode

from .BaseTrackobot import BaseTrackobot
from TrackoBot.utilities import TObject,Workspace
from TrackoBot.Inventory import Inventory

class Trackobot(BaseTrackobot):
    
    def __init__(self, workspace_config, src_config):
        self.workspace = Workspace(workspace_config)
        self.inventory = Inventory(self.workspace)
        self.source_init(src_config)
        self.curr_nObjects = []
        self.prev_nObjects = []
        self.barcodes = []
        super().__init__()
        
    def source_init(self,src_config):
        if src_config["name"] == "Image":
            self.source = cv2.imread(src_config["path"])
        elif src_config["name"] == "Camera":
            self.source = cv2.VideoCapture(src_config["path"])
            self.source.set(3,500)
            self.source.set(4,500)
        return
    
    def getFrame(self):
        try:
            success, img = self.source.read()
        except:
            img = self.source
        return img
    
    def BarcodeDetection(self,img):
        
        
        # for barcode in decode(img):
        #     if barcode not in self.barcodes:
        #         self.barcodes.append(barcode.data.decode('utf-8'))
        
        # print(self.barcodes)
        
        
        
        
        barcodes = []
        bboxes = []
        detected = False
        for barcode in decode(img):
            barcode_number = barcode.data.decode('utf-8')
            polygon = np.array([barcode.polygon],np.int32)
            polygon = polygon.reshape((-1,1,2))
            # cv2.polylines(img,[polygon],True,(255,0,255),5)
            rect = barcode.rect
            detected = True
            if rect != None:
                bboxes.append(rect)
                self.curr_nObjects.append(TObject(rect=rect,polygon=polygon,barcode=barcode_number))
        
        if not detected :
            return
        
        for tobj in self.curr_nObjects :
            self.inventory.addObject(tobj)
        if bboxes != None:
            return bboxes
        # if len(self.prev_nObjects) == len(self.curr_nObjects):
        #     self.curr_nObjects = []
        #     return
        
        # for cObject in self.curr_nObjects:
            
        #     self.inventory.addObject(cObject)

        # cv2.putText(img,barcode_number,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,0,255),2)
        # self.prev_nObjects = []
        # self.prev_nObjects = self.curr_nObjects 
        # self.curr_nObjects = []
        # print(barcodes)
        # barcodes = []
        
    
    def TextRecognition(self):
        pass
    
    def ExpDateRecongition(self):
        pass
    
    def ObjTracker(self):
        pass