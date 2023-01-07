import cv2
import numpy as np
from pyzbar.pyzbar import decode

username = ["Trackobot","admin","Alexandros Mikelis",]
password = ["9883","Koko1234!"]
port = [80,554]


cap = cv2.VideoCapture('http://Trackobot:9883@192.168.1.13:80')

try:
    success, img = cap.read()
    decode(img)
    print("success")
except:
    print("error")