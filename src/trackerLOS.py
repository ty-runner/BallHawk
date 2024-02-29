import cv2
from ultralytics import YOLO

def process_frame(frame, model, prev_positions):
    # Perform detection
    results = model(frame)
    
    # Accessing detection results
    for result in results:
        boxes = result.boxes 
        for box in boxes:
            cords = box.xyxy[0].tolist()
            class_id = box.cls[0].item()
            conf = box.conf[0].item()

            class_name = result.names[class_id]

            if class_name == 'person':
                x1, y1, x2, y2 = map(int, cords)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f'{class_name} {conf:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                person_id = class_id
                
                cv2.putText(frame, f'ID: {person_id}', (x1, y1-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Record current position for breadcrumb trail
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                if person_id in prev_positions:
                    prev_position = prev_positions[person_id][-1]
                    distance = ((center[0] - prev_position[0])**2 + (center[1] - prev_position[1])**2)**0.5
                    # If the distance is less than a threshold, consider it a valid update and record it
                    if distance < 100:
                        prev_positions[person_id].append(center)
                else:
                    # If no previous position is available, initialize with the current position
                    prev_positions[person_id] = [center]
                
                if len(prev_positions[person_id]) > 1:
                    for i in range(1, len(prev_positions[person_id])):
                        cv2.line(frame, prev_positions[person_id][i-1], prev_positions[person_id][i], (0, 255, 0), 2)

    return frame

model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture('test2.mp4')

prev_positions = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = process_frame(frame, model, prev_positions)
    
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()