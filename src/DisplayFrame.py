import cv2

def display_frame(frame, tracks):
    """
    Display a video frame with tracked objects highlighted.

    This function takes a video frame and a list of tracked objects, and displays the frame with bounding boxes 
    and track IDs drawn around the tracked objects. Each tracked object is represented by a rectangle and a label 
    with its track ID.

    Args:
        frame: The video frame to be displayed.
        tracks: A list of tracked objects. Each track object is expected to have a `track_id` attribute and 
                a `to_ltrb` method that returns the bounding box in left-top-right-bottom (LTRB) format.

    Returns:
        None

    Examples:
        >>> frame = cv2.imread('frame.jpg')
        >>> tracks = [track1, track2]
        >>> display_frame(frame, tracks)
    """
    
    track_ids = []
    for track in tracks:
        track_id = track.track_id
        if track_id not in track_ids:
            ltrb = track.to_ltrb()
            print(f"ltrb {ltrb}")
            cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(ltrb[2]), int(ltrb[3])), (255, 0, 0), 2)
            track_ids.append(track_id)
            cv2.putText(frame, str(track_id), (int(ltrb[0]), int(ltrb[1] - 10)), 0, 0.75, (0, 255, 0), 2)
    cv2.imshow('Frame', frame)
