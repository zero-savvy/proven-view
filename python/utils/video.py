# This code converts videos with every resolution to SD, and resize the video with your target fps.
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip


def get_video_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def convert_set_frames(input_video_path: str, output_video_path: str, target_fps: int):
    
    clip = VideoFileClip(input_video_path)
    
    # Set the new fps
    fixed_frame_rate = clip.set_fps(target_fps)
    
    # Write the resized video to a file
    temp_path = "converted_video_fixed_frames.mp4"
    fixed_frame_rate.write_videofile(output_video_path, codec='libx264')
