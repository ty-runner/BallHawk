import cv2
print(cv2.__version__)
import numpy as np
import easyocr
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('PublicModels/yolov8x.pt')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def detect_players(frame, model, conf_threshold=0.5):
    results = model(frame)  # Get results from the model
    print("Complete Results Object:", results)  # Print the complete results object
    print("Results Inspection:", dir(results[0]))  # Inspect methods and attributes of the first item in the results list

    if results:
        print("Names and classes:", results[0].names)  # Print detected class names
        detections = results[0].boxes.xyxy[0]  # Assuming boxes.xyxy[0] is still correct
        print("Detections Tensor:", detections)  # Print the detections tensor

        if detections.nelement() > 0:
            for detection in detections:
                print("Individual Detection:", detection)  # Print each detection component
                if detection.numel() == 6:  # Ensure the tensor for each detection has six elements
                    x1, y1, x2, y2, conf, cls_id = detection.tolist()
                    if conf > conf_threshold and int(cls_id) == 0:
                        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                        boxes.append([x1, y1, x2-x1, y2-y1])
        else:
            print("No detections found or in an unexpected format.")
    else:
        print("No results obtained from the model.")

    return []

def initialize_tracker(frame, boxes):
    trackers = []
    for box in boxes:
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, tuple(box))
        trackers.append(tracker)
    return trackers

def update_trackers(frame, trackers):
    updated_boxes = []
    for tracker in trackers:
        success, box = tracker.update(frame)
        if success:
            updated_boxes.append(box)
    return updated_boxes

def extract_jersey_number(frame, box):
    x, y, w, h = box
    jersey_area = frame[y:y+h, x:x+w]
    results = reader.readtext(jersey_area, allowlist='0123456789')
    numbers = [text for _, text, _ in results if text.isdigit() and int(text) < 100]
    if numbers:
        return str(min(numbers, key=lambda x: len(x)))  # Choose the smallest number (in terms of length)
    return 'Unknown'

# Setup video capture and output
capture = cv2.VideoCapture('TestInputs/wide_23s.mp4')
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
out = cv2.VideoWriter('test2_out.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

first_frame = True
while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    if first_frame:
        # Detect players in the first frame
        boxes = detect_players(frame, model)
        tracker = initialize_tracker(frame, boxes)
        first_frame = False
    else:
        # Update tracker in subsequent frames
        success, boxes = tracker.update(frame)

    # Draw tracking boxes and extract jersey numbers
    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        jersey_number = extract_jersey_number(frame, newbox)
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
        cv2.putText(frame, f'#{jersey_number}', (p1[0], p1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Write frame into the output file
    out.write(frame)

    # Display frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press Q to exit
        break

# When everything is done, release the video capture and video write objects
capture.release()
out.release()
cv2.destroyAllWindows()
