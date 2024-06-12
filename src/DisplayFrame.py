#NEED HEADER
import cv2

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