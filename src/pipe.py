from frame_splicer import splice_frames
from yolo_analysis import analyze_frame
#from player_vectorization import vectorize_players

def process_video(video_path):
    frames = splice_frames(video_path)
    for frame in frames:
        results = analyze_frame(frame)
        # vectorize_players(results)
        # Continue the pipeline

if __name__ == "__main__":
    video_path = 'path_to_your_video.mp4'
    process_video(video_path)
