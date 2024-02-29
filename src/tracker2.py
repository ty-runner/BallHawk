'''
import cv2
import numpy as np
import pytesseract
from ultralytics import YOLO  # Ensure Ultralytics YOLO is correctly installed
import easyocr
reader = easyocr.Reader(['en'])

def get_dominant_color(image, k=1):
    """
    Find the dominant color in the image by applying k-means clustering.
    """
    pixels = np.float32(image.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, palette = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    return dominant

def get_team_color(frame, box):
    """
    Determines the dominant color in the jersey area to classify the team or referee.
    """
    x1, y1, x2, y2 = map(int, box)
    jersey_area = frame[y1:y2, x1:x2]
    dominant_color = get_dominant_color(jersey_area)

    if 20 <= dominant_color[0] <= 30:  # Example range for Team 1
        return 'team1'
    elif 100 <= dominant_color[0] <= 140:  # Example range for Team 2
        return 'team2'
    else:  # Assuming referees or unclassified
        return 'referee'

def preprocess_for_ocr(img):
    """
    Apply preprocessing steps to highlight jersey numbers against contrasting backgrounds.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(thresh, 50, 150)
    dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
    return dilated


def extract_jersey_number(frame, box):
    """
    Attempts to extract the jersey number using OCR on the preprocessed image area.
    """
    x1, y1, x2, y2 = map(int, box)
    jersey_area = frame[y1:y2, x1:x2]
    preprocessed = preprocess_for_ocr(jersey_area)
    text = pytesseract.image_to_string(preprocessed, config='--psm 7 -c tessedit_char_whitelist=0123456789')
    number = ''.join(filter(str.isdigit, text))
    return number if number else 'Unknown'

def extract_jersey_number(frame, box):
    """
    Extracts the jersey number using EasyOCR on the jersey area.
    """
    x1, y1, x2, y2 = map(int, box)
    jersey_area = frame[y1:y2, x1:x2]
    results = reader.readtext(jersey_area, allowlist='0123456789')
    
    # Filter results to only include detected numbers
    numbers = [text for _, text, _ in results]
    return ', '.join(numbers) if numbers else 'Unknown'


def process_frame(frame, model):
    results = model(frame)
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cords = box.xyxy[0].tolist()
            class_id = box.cls[0].item()

            if result.names[class_id] == 'person':  # Process only if detected as a person
                team_color = get_team_color(frame, cords)
                x1, y1, x2, y2 = map(int, cords)
                box_color = (255, 0, 0) if team_color == 'team1' else (0, 0, 255) if team_color == 'team2' else (255, 255, 0)  # Yellow for referees

                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                jersey_number = extract_jersey_number(frame, cords)
                cv2.putText(frame, f'#{jersey_number}', (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

    return frame

# Initialize the model and video source
model = YOLO('yolov8n.pt')  # Specify the correct path to the model
cap = cv2.VideoCapture('test2.mp4')  # Ensure the correct path to your video file

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = process_frame(frame, model)
    
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''

import cv2
import numpy as np
import easyocr
from ultralytics import YOLO  # Ensure Ultralytics YOLO is correctly installed

reader = easyocr.Reader(['en'])

number_history = {}  # {person_id: (number, count, locked)}

def get_dominant_color(image, k=1):
    pixels = np.float32(image.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, palette = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    return dominant

def get_team_color(frame, box):
    x1, y1, x2, y2 = map(int, box)
    jersey_area = frame[y1:y2, x1:x2]
    dominant_color = get_dominant_color(jersey_area)

    if 20 <= dominant_color[0] <= 30:
        return 'team1'
    elif 100 <= dominant_color[0] <= 140:
        return 'team2'
    else:
        return 'referee'

def extract_jersey_number(frame, box):
    x1, y1, x2, y2 = map(int, box)
    jersey_area = frame[y1:y2, x1:x2]
    results = reader.readtext(jersey_area, allowlist='0123456789')
    
    numbers = [int(text) for _, text, _ in results if text.isdigit() and int(text) < 100]
    if numbers:
        return str(min(numbers, key=numbers.count))
    return 'Unknown'

def update_number_history(person_id, number):
    if number == 'Unknown':
        return number
    if person_id in number_history:
        num, count, locked = number_history[person_id]
        if locked:
            return num
        if num == number:
            count += 1
            if count >= 8:
                locked = True
        else:
            count = 1
        number_history[person_id] = (number, count, locked)
    else:
        number_history[person_id] = (number, 1, False)
    return number_history[person_id][0]

def process_frame(frame, model):
    results = model(frame)
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cords = box.xyxy[0].tolist()
            class_id = box.cls[0].item()

            if result.names[class_id] == 'person':
                team_color = get_team_color(frame, cords)
                x1, y1, x2, y2 = map(int, cords)
                box_color = (255, 0, 0) if team_color == 'team1' else (0, 0, 255) if team_color == 'team2' else (255, 255, 0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                person_id = f"{x1}_{y1}"  # Simplified person tracking
                jersey_number = extract_jersey_number(frame, cords)
                jersey_number = update_number_history(person_id, jersey_number)
                cv2.putText(frame, f'#{jersey_number}', (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

    return frame

# Initialize the model and video source
model = YOLO('yolov8n.pt')  # Ensure you have the correct path to the model
cap = cv2.VideoCapture('test2.mp4')  # Ensure you have the correct path to your video file

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = process_frame(frame, model)
    
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
