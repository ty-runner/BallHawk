import cv2
from ultralytics import YOLO
from process_frames import process_frame

def process_video(video_path, output_path):
    model = YOLO("yolov8n.pt")  #8n is lightest one, may need to look into trainer our own
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  #codec
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame = process_frame(frame, model)
        
        out.write(processed_frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    video_path = 'test2.mp4'  # Input video path
    output_path = 'test2_output.mp4'  # Output video path
    process_video(video_path, output_path)
