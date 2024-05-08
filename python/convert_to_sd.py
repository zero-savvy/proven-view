# This code converts videos with every resolution to SD, and resize the video with your target fps.
import tkinter as tk
from tkinter import filedialog

from moviepy.editor import VideoFileClip

def get_video_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def convert_to_sd(input_video_path, output_video_path, start_time, end_time, target_fps):
    # Load the video file
    clip = VideoFileClip(input_video_path)
    print("Original Video Info:")
    print(f"Resolution: {clip.size[0]}x{clip.size[1]}")
    print(f"Frame Rate: {clip.fps}")

    # Trim the video from start_time to end_time
    trimmed_clip = clip.subclip(start_time, end_time)

    # Target resolution for SD (max height or width for SD)
    max_width = 640
    max_height = 480

    # Calculate the new dimensions while maintaining the aspect ratio
    original_width, original_height = clip.size
    aspect_ratio = original_width / original_height
    
    if original_width / original_height > max_width / max_height:
        # Width is the constraining dimension
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
    else:
        # Height is the constraining dimension
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    # Resize the video
    resized_clip = trimmed_clip.resize(newsize=(new_width, new_height))

    if clip.fps > target_fps:
        # Set the new fps
        resized_clip = resized_clip.set_fps(target_fps)
    
    # Write the resized video to a file
    resized_clip.write_videofile(output_video_path, codec='libx264')

# Example usage
video_path = get_video_path()
output_video = 'output_video_sd.mp4'
start_time = 1  # Start time in seconds or (min, sec) tuple
end_time = 3    # End time in seconds or (min, sec) tuple
convert_to_sd(video_path, output_video, start_time, end_time, 30)
