import requests
import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
Barcodes=[]
while True:
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        if myData not in Barcodes:
            Barcodes.append(str(myData))
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


endpoint = "http://127.0.0.1:8000/api/products/" 

data= {}
for barcode in Barcodes:
    data["title"] = barcode
    get_response = requests.post(endpoint, json=data) 

print(get_response.json())