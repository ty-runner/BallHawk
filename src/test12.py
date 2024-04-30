import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
#from tracker2 import *
model = YOLO('yolov8n.pt')
deepsort = DeepSort(max_age=30)

#cap = cv2.VideoCapture('WideWide_-_Clip_027_copy.mp4')
# cap = cv2.VideoCapture('tt1.mp4')
cap = cv2.VideoCapture('WideWide_-_Clip_027_copy.mp4')
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
    track_info = tuple(zip(bbox_xywh, confidences, class_ids))
    tracks = deepsort.update_tracks(track_info, frame=frame)
    track_ids = []
    if bbox_xywh:
        for track in tracks:
            track_id = track.track_id
            if track_id not in track_ids:
                ltrb = track.to_ltrb()
                print(f"ltrb ${ltrb}")
                cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(ltrb[2]), int(ltrb[3])), (255, 0, 0), 2)
                track_ids.append(track_id)
                cv2.putText(frame, str(track_id), (int(ltrb[0]), int(ltrb[1] - 10)), 0, 0.75, (0, 255, 0), 2)
    cv2.imshow('Frame', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
