import cv2
import sys

def get_video_info(filename: str) -> dict:
    """
    Retrieve video information.

    Given a filename of a video file, this function retrieves the video's frame count, frames per second (fps), 
    frame width, and frame height.

    Args:
        filename (str): The path to the video file.

    Returns:
        dict: A dictionary containing the video's frame count, fps, frame width, and frame height.
              Returns None if the video file cannot be opened.

    Examples:
        >>> get_video_info('video.mp4')
        {'frame_count': 1500, 'fps': 30, 'frame_width': 1920, 'frame_height': 1080}
    """
    
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return None
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cap.release()
    
    video_info = {
        "frame_count": frame_count,
        "fps": fps,
        "frame_width": frame_width,
        "frame_height": frame_height
    }
    
    return video_info

def calculate_sharpness(frame) -> float:
    """
    Calculate the sharpness of a video frame.

    Given a video frame, this function calculates its sharpness using the variance of the Laplacian.

    Args:
        frame: A single video frame.

    Returns:
        float: The sharpness value of the frame.

    Examples:
        >>> calculate_sharpness(frame)
        100.45
    """
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = laplacian.var()
    return sharpness

def assess_clarity(video_file: str) -> float:
    """
    Assess the clarity of a video file.

    Given a video file, this function calculates the average sharpness of its frames.

    Args:
        video_file (str): The path to the video file.

    Returns:
        float: The average sharpness of the video frames.

    Examples:
        >>> assess_clarity('video.mp4')
        120.67
    """
    
    cap = cv2.VideoCapture(video_file)
    total_sharpness = 0
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        sharpness = calculate_sharpness(frame)
        print("Sharpness:", sharpness)
        total_sharpness += sharpness
        frame_count += 1

    cap.release()
    average_sharpness = total_sharpness / frame_count
    return average_sharpness

def calculate_quality_score(video_info: dict) -> float:
    """
    Calculate the quality score of a video.

    Given the video information, this function calculates a quality score based on the video's fps and clarity.

    Args:
        video_info (dict): A dictionary containing the video's frame count, fps, frame width, and frame height.

    Returns:
        float: The calculated quality score.

    Examples:
        >>> calculate_quality_score({'frame_count': 1500, 'fps': 30, 'frame_width': 1920, 'frame_height': 1080})
        85.6
    """
    
    clarity_score = assess_clarity(sys.argv[1])
    score = 100
    fps_scale = min(video_info["fps"] / 30, 1)
    clarity_scale = clarity_score / 100 if clarity_score < 100 else 1
    print(video_info)
    print("Clarity Score:", clarity_score)
    print("FPS Scale:", fps_scale)
    score = score * ((0.3 * fps_scale) + (0.7 * clarity_scale)) # add weighting for clarity
    return score

def main():
    """
    Main function to assess video quality.

    This function retrieves the video information and calculates the quality score. It prints the quality score
    and provides recommendations based on the score.

    Examples:
        >>> main()
        Quality Score: 78.5
        Video quality is safe for processing
    """
    
    filename = sys.argv[1]
    video_info = get_video_info(filename)
    
    if video_info:
        quality_score = calculate_quality_score(video_info)
        print("Quality Score:", quality_score)
        if quality_score > 70:
            print("Video quality is safe for processing")
        elif quality_score < 50:
            print("Video quality is poor, consider using a higher quality video. Possible errors in processing")
    else:
        print("Failed to retrieve video information.")

if __name__ == "__main__":
    main()
