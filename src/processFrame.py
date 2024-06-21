def process_frame(model, frame):
    """
    Process a video frame using a YOLO model to detect objects.

    This function processes a single video frame using a given YOLO model to detect objects. It extracts bounding boxes, 
    confidence scores, and class IDs for detected objects. Only objects of a specific class (e.g., class ID 0) with a 
    confidence score greater than 0.6 are considered.

    Args:
        model: The YOLO model used for object detection.
        frame: The video frame to be processed.

    Returns:
        tuple: A tuple containing three lists:
            - bbox_xywh (list): A list of bounding boxes in xywh format (x, y, width, height).
            - confidences (list): A list of confidence scores for each detected object.
            - class_ids (list): A list of class IDs for each detected object.

    Examples:
        >>> model = YOLO('path/to/yolo_model')
        >>> frame = cv2.imread('frame.jpg')
        >>> process_frame(model, frame)
        ([[10, 20, 30, 40]], [0.75], [0])
    """
    
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
