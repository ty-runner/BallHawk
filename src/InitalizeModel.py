import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

#Need Header

def initialize_model(model_path):
    model = YOLO(model_path)
    deepsort = DeepSort(max_age=30)
    return model, deepsort