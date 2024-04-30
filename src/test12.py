import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

model = YOLO('yolov8n.pt')
deepsort = DeepSort(max_age=30, nn_budget=100, override_track_class=None)

cap = cv2.VideoCapture('tt1.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    bbox_xywh = []
    confidences = []
    class_ids = []

    for result in results:
        if hasattr(result, 'boxes'):
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = box.conf.item()
                cls_id = int(box.cls.item())

                if cls_id == 0 and conf > 0.6:
                    bbox = [x1, y1, x2 - x1, y2 - y1]  #xywh
                    bbox_xywh.append(bbox)
                    confidences.append(conf)
                    class_ids.append(cls_id)

    if bbox_xywh:
        try:
            tracks = deepsort.update_tracks(bbox_xywh, confidences, class_ids, frame)
            # Draw the tracks
            for track in tracks:
                if not track.is_confirmed() or track.time_since_update > 1:
                    continue
                bbox = track.to_tlbr()
                track_id = track.track_id
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 255, 255), 2)
                cv2.putText(frame, str(track_id), (int(bbox[0]), int(bbox[1] - 10)), 0, 0.75, (0, 255, 0), 2)
        except Exception as e:
            print("Error updating tracks:", str(e))
    else:
        print("No valid detections.")

    cv2.imshow('Frame', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
