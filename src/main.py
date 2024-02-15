import tkinter as tk
from tkinter import filedialog
import os
from uploader import process_video
from pytube import YouTube

current_path = os.getcwd()
print("Current path:", current_path)

def download_video(url):
    yt = YouTube(url)
    # Select the highest resolution stream available
    video_stream = yt.streams.get_highest_resolution()
    # Download the video to the current directory
    video_stream.download(current_path)
    # Return the file path of the downloaded video
    return os.path.join(current_path, video_stream.default_filename)

def upload_video():
    # Prompt the user to enter the YouTube URL
    url = input("Enter the YouTube URL: ")
    # Download the video
    file_path = download_video(url)
    # Process the downloaded video
    process_video(file_path)

root = tk.Tk()
root.title("Video Upload and Processing")

upload_button = tk.Button(root, text="Upload YouTube Video", command=upload_video)
upload_button.pack(pady=20)

root.mainloop()
