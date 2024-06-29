import cv2
import numpy as np
import easyocr
from ultralytics import YOLO

'''
0: 384x640 29 persons, 1 horse, 57.4ms
Speed: 3.5ms preprocess, 57.4ms inference, 1.0ms postprocess per image at shape (1, 3, 384, 640)
Detections shape: torch.Size([4])
Detections content: tensor([883.0917, 264.2418, 975.2848, 550.7069])
Detection: 883.0917358398438
Traceback (most recent call last):
  File "/Users/michael/Desktop/Snr Design/ECE-49595-Proj/src/allin2.py", line 71, in <module>
    boxes = detect_players(frame, model)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michael/Desktop/Snr Design/ECE-49595-Proj/src/allin2.py", line 22, in detect_players
    if detection[4] > conf_threshold and int(detection[5]) == 0:  # Check confidence and class
       ~~~~~~~~~^^^
IndexError: index 4 is out of bounds for dimension 0 with size 0
'''

# Load YOLOv8 model
model = YOLO('PublicModels/yolov8n.pt')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def detect_players(frame, model, conf_threshold=0.5):
    results = model(frame)
    boxes = []
    if results and hasattr(results[0], 'boxes'):
        detections = results[0].boxes.xyxy[0]  # Assuming this is the correct way to access detections
        print(f"Detections shape: {detections.shape}")  # Debug the shape
        print(f"Detections content: {detections}")  # Check what's actually inside
        if detections.shape[0] > 0:
            for detection in detections:
                print(f"Detection: {detection}")  # Detailed look at each detection
                if detection[4] > conf_threshold and int(detection[5]) == 0:  # Check confidence and class
                    x1, y1, x2, y2 = map(int, detection[:4])
                    boxes.append((x1, y1, x2-x1, y2-y1))
        else:
            print("No detections found.")
    else:
        print("No results or malformed results structure.")
    return boxes

def initialize_trackers(frame, boxes):
    trackers = []
    for box in boxes:
        tracker = cv2.TrackerCSRT_create()
        trackers.append(tracker)
        tracker.init(frame, tuple(box))
    return trackers

def update_trackers(frame, trackers):
    boxes = []
    for tracker in trackers:
        success, box = tracker.update(frame)
        if success:
            boxes.append(box)
    return boxes

def extract_jersey_number(frame, box):
    x, y, w, h = map(int, box)
    jersey_area = frame[y:y+h, x:x+w]
    results = reader.readtext(jersey_area)
    if results:
        numbers = sorted((text for _, text, _ in results if text.isdigit()), key=len)
        if numbers:
            return numbers[0]
    return 'Unknown'

capture = cv2.VideoCapture('TestInputs/wide_23s.mp4')
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
out = cv2.VideoWriter('test2_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

trackers = []
first_frame = True

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    if first_frame:
        boxes = detect_players(frame, model)
        trackers = initialize_trackers(frame, boxes)
        first_frame = False
    else:
        boxes = update_trackers(frame, trackers)

    for box in boxes:
        p1 = (int(box[0]), int(box[1]))
        p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)
        jersey_number = extract_jersey_number(frame, box)
        cv2.putText(frame, f'#{jersey_number}', (p1[0], p1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    out.write(frame)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
out.release()
cv2.destroyAllWindows()
