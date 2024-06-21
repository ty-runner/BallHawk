import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

def initialize_model(model_path: str) -> tuple:
    """
    Initialize the YOLO model and DeepSort tracker.

    Given the file path to a pre-trained YOLO model, this function initializes the YOLO model and a DeepSort tracker.

    Args:
        model_path (str): The file path to the pre-trained YOLO model.

    Returns:
        tuple: A tuple containing the initialized YOLO model and DeepSort tracker.

    Examples:
        >>> initialize_model('path/to/yolo_model')
        (<YOLO model object>, <DeepSort tracker object>)
    """
    
    model = YOLO(model_path)
    deepsort = DeepSort(max_age=30)
    return model, deepsort
