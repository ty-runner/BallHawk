#PLACEHOLDER FOR SUPERSCALE
from ultralytics import YOLO

model = YOLO("yolov8n.pt") 

# Predict on an image or frame
results = model("path_to_your_frame.jpg")
#results.show()
