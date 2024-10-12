import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
from lp_image import process_image
from webcam import process_video
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess


def open_file():
    file_path = filedialog.askopenfilename(
        title="Select Image or Video",
        filetypes=(("Image Files", "*.jpg;*.jpeg;*.png;*.bmp"),("Video Files", "*.mp4;*.avi;*.mov"),("All Files", "*.*")))
    
    if file_path:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            try:
                process_image(file_path)  
                messagebox.showinfo("Success", "Image processing completed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            try:
                process_video(file_path)  
                messagebox.showinfo("Success", "Video processing completed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select a valid image or video file.")

root = tk.Tk()
root.title("Image/Video Processor")

btn_open = tk.Button(root, text="Open Image/Video", command=open_file)
btn_open.pack(pady=20)

root.mainloop()
