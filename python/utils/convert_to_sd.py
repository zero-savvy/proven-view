# This code converts videos with every resolution to SD, and resize the video with your target fps.
import tkinter as tk
from tkinter import filedialog
import ffmpeg

from moviepy.editor import VideoFileClip, clips_array, ImageSequenceClip
import numpy as np
from moviepy.video.fx import resize
import os

def get_video_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def convert_to_sd(input_video_path, output_video_path, target_fps):
    
    clip = VideoFileClip(input_video_path)
    
    if clip.size[1] > clip.size[0]:
        # Rotate the video by 90 degrees if it's portrait
        clip = clip.rotate(90)

    target_width = 640
    target_height = 480

    # Calculate the new dimensions while maintaining the aspect ratio
    original_width, original_height = clip.size
    aspect_ratio = original_width / original_height
    
    if aspect_ratio > target_width / target_height:
        # Width is the constraining dimension
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    else:
        # Height is the constraining dimension
        new_height = target_height
        new_width = int(new_height * aspect_ratio)

    # Resize the video
    resized_clip = clip.resize(newsize=(new_width, new_height))

    # Set the new fps
    resized_clip = resized_clip.set_fps(int(min(target_fps, clip.fps)))
    
    # Write the resized video to a file
    temp_path = "temp_resized_vid.mp4"
    resized_clip.write_videofile(temp_path, codec='libx264')

    v = ffmpeg.input(temp_path)
    kwargs = {
        'w':str(target_width), 
        'h':str(target_height), 
        'x':'0' if target_width == new_width else str(int((target_width - new_width) / 2)), 
        'y':'0' if target_height == new_height else str(int((target_height - new_height) / 2)), 
        'color':'black@0'}
    v_pad = ffmpeg.filter(v, filter_name='pad', **kwargs)
    v_pad.output(output_video_path).run()

    os.remove(temp_path)
    

if __name__ == "__main__":
    # Example usage
    video_path = get_video_path()
    output_video = 'output_video_sd.mp4'
    start_time = 1  # Start time in seconds or (min, sec) tuple
    end_time = 3    # End time in seconds or (min, sec) tuple
    convert_to_sd(video_path, output_video, start_time, end_time, 30)


    # trimmed_frames = []
    # for i, frame in enumerate(clip.iter_frames()):
    #     if i < int(start_time * clip.fps):
    #         continue
    #     if i > int(end_time * clip.fps):
    #         break
    #     trimmed_frames.append(frame)

    # trimmed_clip = ImageSequenceClip([frame for frame in trimmed_frames], fps=clip.fps)
