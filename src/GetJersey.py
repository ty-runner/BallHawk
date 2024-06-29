import cv2
import numpy as np
import pytesseract
import easyocr

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

def preprocess_for_ocr(img):
    """
    Apply preprocessing steps to highlight jersey numbers against contrasting backgrounds.

    Args:
        img (numpy.ndarray): The input image in which to preprocess for OCR.

    Returns:
        numpy.ndarray: The preprocessed image with highlighted features for OCR.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(thresh, 50, 150)
    dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
    return dilated

def extract_jersey_number(frame, box):
    """
    Attempts to extract the jersey number using OCR on the preprocessed image area.

    Args:
        frame (numpy.ndarray): The input image frame containing the jersey.
        box (tuple): A tuple containing four integers (x1, y1, x2, y2) which define the bounding box
                     of the jersey area within the frame.

    Returns:
        str: The extracted jersey number as a string. Returns 'Unknown' if no number is detected.
    """
    x1, y1, x2, y2 = map(int, box)
    jersey_area = frame[y1:y2, x1:x2]
    preprocessed = preprocess_for_ocr(jersey_area)
    text = pytesseract.image_to_string(preprocessed, config='--psm 7 -c tessedit_char_whitelist=0123456789')
    number = ''.join(filter(str.isdigit, text))
    return number if number else 'Unknown'

def extract_jersey_number_easyocr(frame, box):
    """
    Extracts the jersey number using EasyOCR on the jersey area.

    Args:
        frame (numpy.ndarray): The input image frame containing the jersey.
        box (tuple): A tuple containing four integers (x1, y1, x2, y2) which define the bounding box
                     of the jersey area within the frame.

    Returns:
        str: The extracted jersey number(s) as a string. Returns 'Unknown' if no number is detected.
    """
    x1, y1, x2, y2 = map(int, box)
    jersey_area = frame[y1:y2, x1:x2]
    results = reader.readtext(jersey_area, allowlist='0123456789')
    
    # Filter results to only include detected numbers
    numbers = [text for _, text, _ in results]
    return ', '.join(numbers) if numbers else 'Unknown'
