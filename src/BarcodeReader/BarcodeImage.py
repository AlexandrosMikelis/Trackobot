import cv2
import numpy as np
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt

img = cv2.imread('./data/image00003.jpeg')

barcodes = decode(img)

for barcode in barcodes:
    	# extract the bounding box location of the barcode and draw the
	# bounding box surrounding the barcode on the image
	(x, y, w, h) = barcode.rect
	cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
	# the barcode data is a bytes object so if we want to draw it on
	# our output image we need to convert it to a string first
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type
	# draw the barcode data and barcode type on the image
	text = "{} ({})".format(barcodeData, barcodeType)
	cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 2)
	# print the barcode type and data to the terminal
	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
# show the output image
cv2.namedWindow('BarTrack', cv2.WINDOW_KEEPRATIO)
cv2.imshow('BarTrack', img)
cv2.resizeWindow('BarTrack', 600, 400)
cv2.waitKey(0)