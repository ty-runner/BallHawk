import cv2
import torch

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_players(frame, model, conf_threshold=0.25):
    # Convert frame from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Perform inference
    results = model(frame_rgb, size=640)
    
    # Parse the detection results
    boxes = []
    for *xyxy, conf, cls in results.xyxy[0]:
        if conf > conf_threshold:
            x1, y1, x2, y2 = map(int, xyxy)
            boxes.append((x1, y1, x2 - x1, y2 - y1))  # Convert to x,y,w,h format
    return boxes

def update_trackers(trackers, frame):
    boxes = []
    for tracker in trackers:
        success, box = tracker.update(frame)
        if success:
            boxes.append(box)
    return boxes

def create_trackers_for_boxes(boxes, frame):
    trackers = []
    for box in boxes:
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, tuple(box))
        trackers.append(tracker)
    return trackers

# Initialize video capture with a video file instead of a camera
capture = cv2.VideoCapture("test_data/people-detection.mp4")
trackers = []
first_frame = True
frame_count = 0
detection_interval = 30  # Run detection every 30 frames

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    if first_frame or frame_count % detection_interval == 0:
        # Clear existing trackers and detect anew
        trackers.clear()
        boxes = detect_players(frame, model)
        trackers = create_trackers_for_boxes(boxes, frame)
        first_frame = False
    else:
        # Update all trackers
        boxes = update_trackers(trackers, frame)

    # Draw boxes for visualization
    for box in boxes:
        p1 = (int(box[0]), int(box[1]))
        p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
        cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)

    # Display the frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

# Release the video capture object and close all windows
capture.release()
cv2.destroyAllWindows()
