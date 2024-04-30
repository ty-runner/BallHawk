import cv2
from ultralytics import YOLO

# Load the pretrained YOLOv8 model
model = YOLO('yolov8n.pt')  # Verify this path to your model file

# Initialize video source
cap = cv2.VideoCapture('tt1.mp4')

points = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform prediction using the model
    results = model(frame)

    # Process each detection in the results
    for result in results:
        # Check if there are boxes and handle them
        if hasattr(result, 'boxes'):
            for box in result.boxes:
                # Check if the tensor has the expected shape
                if box.xyxy.shape[0] == 1 and box.xyxy.shape[1] == 4:
                    x1, y1, x2, y2 = box.xyxy[0]  # Extract all four elements at once
                    conf = box.conf
                    cls_id = box.cls

                    if cls_id == 0 and conf > 0.6:  # Assuming 'person' class is ID 0
                        center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                        points.append(center)

                        # Draw the trail
                        for j in range(1, len(points)):
                            if points[j - 1] and points[j]:
                                cv2.line(frame, points[j - 1], points[j], (0, 255, 0), 3)

    # Show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
