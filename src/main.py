# main.py
import tkinter as tk
from tkinter import filedialog
import os
from uploader import process_video
"""
Super outdated code, but it's just a placeholder for the main.py file.
"""
current_path = os.getcwd()
print("Current path:", current_path)

def upload_video():
    file_path = filedialog.askopenfilename()
    process_video(file_path)

root = tk.Tk()
root.title("Video Upload and Processing")

upload_button = tk.Button(root, text="Upload Video", command=upload_video)
upload_button.pack(pady=20)

root.mainloop()

