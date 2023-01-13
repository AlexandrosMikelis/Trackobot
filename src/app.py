from TrackoBot import Trackobot
import cv2

def main():
    trackobot = Trackobot(123,{"name":"Camera","path":1})
    bboxes = []
    while True:
        frame = trackobot.getFrame()
        bboxes.append(trackobot.BarcodeDetection(frame))
            
        cv2.imshow("Trackobot",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    trackobot.inventory.display()
    print(bboxes)
if __name__ == "__main__":
    main()