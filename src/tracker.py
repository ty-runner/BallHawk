import cv2

def initialize_tracker(frame, boxes):
    trackers = cv2.MultiTracker_create()
    for box in boxes:
        trackers.add(cv2.TrackerCSRT_create(), frame, tuple(box))
    return trackers

def detect_players(frame, net, output_layers, conf_threshold=0.5):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def process_video(video_path):
# Create video cap object
    capture = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not capture.isOpened():
        print("Error: Could not open video.")
        exit()

    # Create background subtractor object
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

    # Read until video is completed
    while capture.isOpened():
        # Capture frame-by-frame
        ret, frame = capture.read()
        if ret:

    # Noise reduction using Gaussian Blur
            frame = cv2.GaussianBlur(frame, (5, 5), 0)

            # Apply background subtraction
            fg_mask = background_subtractor.apply(frame)

            # Display the original frame
            cv2.imshow('Original Frame', frame)

            # Display the foreground mask
            cv2.imshow('Foreground Mask', fg_mask)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break


    # When everything done, release the video capture object
    capture.release()

    # Closes all the frames
    cv2.destroyAllWindows()


first_frame = True
while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    if first_frame:
        # Detect players in the first frame
        boxes = detect_players(frame, net, output_layers)
        tracker = initialize_tracker(frame, boxes)
        first_frame = False
    else:
        # Update tracker in subsequent frames
        success, boxes = tracker.update(frame)

        # Draw tracking boxes
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)

    # Display frame
    cv2.imshow("Frame", frame)
    

    #Finsh processing here

# When everything done, release the video capture object
capture.release()

# Closes all the frames
cv2.destroyAllWindows()
