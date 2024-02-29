'''
from ultralytics import YOLO
import cv2
import numpy as np
import pandas as pd

# Assuming the model is initialized outside this function to avoid reloading it for each frame
model = YOLO('yolov8n.pt')  # Load a pretrained model

def process_frame(frame):
    # Perform detection on the frame
    results = model(frame)

    # Access detections; this part needs to be aligned with the actual structure of `results`
    # Assuming `results.xyxy[0]` contains the detections if `results.pred[0]` fails
    detections = results.xyxy[0] if hasattr(results, 'xyxy') else []
    print('CHECK3')

    for det in detections:
        # Extract bounding box coordinates and class ID
        x1, y1, x2, y2, conf, cls = map(int, det[:4].tolist() + det[4:6].tolist())
        label = results.names[cls]
        print('CHECK2')
        
        # Check if the detected class is 'person'
        if label == 'person':
            print('CHECK')
            # Draw rectangle around each 'person' detected
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # Optionally, add label and confidence score
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    return frame
'''
from ultralytics import YOLO
import cv2

# Assuming the model is initialized outside this function
#model = YOLO('yolov8n.pt')  # Load the pretrained model

def process_frame(frame, model):
    # Perform detection
    results = model(frame)
    
    # Accessing detection results
    for result in results:
        boxes = result.boxes  # Access detected bounding boxes
        for box in boxes:
            # Unpack the bounding box coordinates and other information
            cords = box.xyxy[0].tolist()
            class_id = box.cls[0].item()
            conf = box.conf[0].item()

            # Convert class ID to class name
            class_name = result.names[class_id]

            # Draw bounding box and label on the frame
            if class_name == 'person':
                x1, y1, x2, y2 = map(int, cords)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f'{class_name} {conf:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    return frame

