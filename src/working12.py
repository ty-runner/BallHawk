import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from CalculateCenter import calculate_center

#####
#This is test12 that has now been functioned out, I would like to eventually
#split this out as we do pipe and filter

#This function is also relian n calc center

#CURRENT FUNC: Applies "sticky" numbers to boxes, and returns center coords that the end

#TO WORK ON: The numbers simply iterate if a player is lost for even a frame
#This might be easily fixes by using OCR for player numbers

def initialize_model(model_path='PublicModels/yolov8n.pt'):
    model = YOLO(model_path)
    deepsort = DeepSort(max_age=30)
    return model, deepsort

def process_frame(model, frame):
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
                    bbox = [x1, y1, x2 - x1, y2 - y1]  # xywh
                    bbox_xywh.append(bbox)
                    confidences.append(conf)
                    class_ids.append(cls_id)

    return bbox_xywh, confidences, class_ids

def update_tracks(deepsort, track_info, frame):
    tracks = deepsort.update_tracks(track_info, frame=frame)
    return tracks

def display_frame(frame, tracks):
    track_ids = []
    for track in tracks:
        track_id = track.track_id
        if track_id not in track_ids:
            ltrb = track.to_ltrb()
            print(f"ltrb {ltrb}")
            cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(ltrb[2]), int(ltrb[3])), (255, 0, 0), 2)
            track_ids.append(track_id)
            cv2.putText(frame, str(track_id), (int(ltrb[0]), int(ltrb[1] - 10)), 0, 0.75, (0, 255, 0), 2)
    cv2.imshow('Frame', frame)

def main(video_path='TestInputs/wide_23s.mp4'):
    
    centers = [] #This may need to be a different format/handling for eff
    #^ Maybe handle as dictionary?

    model, deepsort = initialize_model()
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        bbox_xywh, confidences, class_ids = process_frame(model, frame)
        track_info = tuple(zip(bbox_xywh, confidences, class_ids))
        tracks = update_tracks(deepsort, track_info, frame)

        for bbox in bbox_xywh:
            center = calculate_center(bbox)
            centers.append(center)

        display_frame(frame, tracks)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Centers of bounding boxes:", centers)

if __name__ == "__main__":
    main()
