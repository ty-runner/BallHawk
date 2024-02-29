import cv2
from ultralytics import YOLO

def process_frame(frame, model, prev_positions):
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

                # Get the unique ID for the person based on their class ID
                person_id = class_id
                
                # Print unique ID next to the player
                cv2.putText(frame, f'ID: {person_id}', (x1, y1-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Record current position for breadcrumb trail
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                prev_positions.setdefault(person_id, []).append(center)
                
                # Draw breadcrumb trail
                if len(prev_positions[person_id]) > 1:
                    for i in range(1, len(prev_positions[person_id])):
                        cv2.line(frame, prev_positions[person_id][i-1], prev_positions[person_id][i], (0, 255, 0), 2)

    return frame

# Load YOLO model
model = YOLO('yolov8n.pt')

# Initialize video source
cap = cv2.VideoCapture('test2.mp4')

# Dictionary to store previous positions of detected persons
prev_positions = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame
    frame = process_frame(frame, model, prev_positions)
    
    # Display the frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()