import cv2
import numpy as np

def get_dominant_color(image, k=1):
    """
    Find the dominant color in the image by applying k-means clustering.

    Args:
        image (numpy.ndarray): The input image from which to find the dominant color.
        k (int): The number of clusters to form. Defaults to 1.

    Returns:
        numpy.ndarray: The dominant color in the image as a BGR tuple.
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

    Args:
        frame (numpy.ndarray): The input image frame containing the jersey.
        box (tuple): A tuple containing four integers (x1, y1, x2, y2) which define the bounding box
                     of the jersey area within the frame.

    Returns:
        str: The classification of the dominant color as 'team1', 'team2', or 'referee'.
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
