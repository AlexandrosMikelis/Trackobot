import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture('rtsp://Trackobot:trackobot123!@192.168.1.14:554/stream2')
print(type(cap))
if cap :
    cap.set(3,500)
    cap.set(4,500)

    while True:
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            print(myData)
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img,[pts],True,(255,0,255),5)
            pts2 = barcode.rect

            cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,0,255),2)
            print(barcode.rect,barcode.polygon)
        cv2.imshow('Result', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break