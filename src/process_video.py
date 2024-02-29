import cv2
from ultralytics import YOLO
from process_frames import process_frame

def process_video(video_path, output_path):
    model = YOLO("yolov8n.pt")  #8n is lightest one, may need to look into trainer our own
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  #codec
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % 5 == 0:
            processed_frame = process_frame(frame, model)

        frame_count += 1
        
        out.write(processed_frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    video_path = 'test2.mp4'  # Input video path
    output_path = 'test2_output.mp4'  # Output video path
    process_video(video_path, output_path)

'''
import cv2
from ultralytics import YOLO
from process_frames import process_frame

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process every frame (remove the conditional to process every frame)
        processed_frame = process_frame(frame)

        # Debugging: Save every 30th frame to disk for verification
        if frame_count % 30 == 0:
            cv2.imwrite(f'debug_frame_{frame_count}.jpg', processed_frame)
            print(f'Saved debug_frame_{frame_count}.jpg')  # Optional: print statement to confirm saving
        
        out.write(processed_frame)
        frame_count += 1

    cap.release()
    out.release()

if __name__ == "__main__":
    video_path = 'test2.mp4'  # Input video path
    output_path = 'test2_output.mp4'  # Output video path
    process_video(video_path, output_path)

'''