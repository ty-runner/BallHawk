import cv2
from ultralytics import YOLO

def process_frame(frame, model):
    results = model(frame)
    
    for *xyxy, conf, cls in results.xyxy[0]:
        if results.names[int(cls)] == 'person': #checking if the detected object is a person
            x1, y1, x2, y2 = map(int, xyxy)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box around the player
    return frame
