'''
import cv2
from ultralytics import YOLO

def process_frame(frame, model):
    results = model(frame)
    
    for *xyxy, conf, cls in results.xyxy[0]:
        if results.names[int(cls)] == 'person': #checking if the detected object is a person
            x1, y1, x2, y2 = map(int, xyxy)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box around the player
    return frame
'''

import cv2
from ultralytics import YOLO

def process_frame(frame, model):
    results = model(frame)
    
    # Assuming results.xyxy[0] is a tensor, convert it to numpy array for cv2.rectangle
    detections = results.xyxy[0].cpu().numpy()  # Convert results to numpy array if not already
    
    for detection in detections:
        x1, y1, x2, y2, conf, cls = map(int, detection[:6])
        if results.names[int(cls)] == 'person':
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    
    return frame
