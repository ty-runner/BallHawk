import cv2
import sys

def get_video_info(filename):
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

def calculate_sharpness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = laplacian.var()
    return sharpness

def assess_clarity(video_file):
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

def calculate_quality_score(video_info):
    # WE CAN TWEAK AS NEEDED, NEED TO TEST ON POOR QUALITY VIDEOS
    # Calculate sharpness score
    clarity_score = assess_clarity(sys.argv[1])
    score = 100
    fps_scale = min(video_info["fps"] / 30, 1)
    if clarity_score < 100:
        clarity_scale = clarity_score / 100
    else:
        clarity_scale = 1
    print(video_info)
    print("Clarity Score:", clarity_score)
    print("FPS Scale:", fps_scale)
    score = score * ((0.3 * fps_scale) + (0.7 * clarity_scale)) # add weighting for clarity
    return score

def main():
    filename = sys.argv[1]
    video_info = get_video_info(filename)
    
    if video_info:
        quality_score = calculate_quality_score(video_info)
        print("Quality Score:", quality_score)
    else:
        print("Failed to retrieve video information.")

if __name__ == "__main__":
    main()
