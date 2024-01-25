import cv2

#video_path = 'test_data/people-detection.mp4'

def process_video(video_path):
# Create video cap object
    capture = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not capture.isOpened():
        print("Error: Could not open video.")
        exit()

    # Create background subtractor object
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

    # Read until video is completed
    while capture.isOpened():
        # Capture frame-by-frame
        ret, frame = capture.read()
        if ret:

    # Noise reduction using Gaussian Blur
            frame = cv2.GaussianBlur(frame, (5, 5), 0)

            # Apply background subtraction
            fg_mask = background_subtractor.apply(frame)

            # Display the original frame
            cv2.imshow('Original Frame', frame)

            # Display the foreground mask
            cv2.imshow('Foreground Mask', fg_mask)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break


    # When everything done, release the video capture object
    capture.release()

    # Closes all the frames
    cv2.destroyAllWindows()
