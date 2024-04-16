#DELETE

from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # Make sure you have the correct path or use a pre-trained model available in their repository

# Inference with a YouTube video URL
video_url = 'https://www.youtube.com/watch?v=AykkITST_Pc'

# Perform inference on the video
results = model(video_url)

# Display results
results.show()  # This will display the video with detections in a new window

# Optionally, save the result. This will save the video with annotations.
results.save('path/to/save/annotated_video.mp4')  # Specify the path where you want to save the annotated video
