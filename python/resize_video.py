# This code converts videos with every resolution to SD, and resize the video with your target fps.
import os

import tkinter as tk
from tkinter import filedialog

import numpy as np
import ffmpeg
import cv2
from moviepy.editor import VideoFileClip, VideoClip

import matplotlib.pyplot as plt


def get_video_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def plot_images_side_by_side_auto_size(np_image1, np_image2):
    """
    Plot two NumPy array images side by side as subfigures using matplotlib.
    Adjusts the figure size based on the dimensions of the input images.

    Args:
    np_image1 (numpy.ndarray): The first input image as a NumPy array.
    np_image2 (numpy.ndarray): The second input image as a NumPy array.
    title1 (str): The title for the first subfigure.
    title2 (str): The title for the second subfigure.

    Returns:
    None
    """
    height1, width1 = np_image1.shape[:2]
    height2, width2 = np_image2.shape[:2]

    # Calculate the total width and maximum height of the two images
    total_width = width1 + width2
    max_height = max(height1, height2)

    desired_width = 1000  # Pixels

    scaling_factor = desired_width / total_width

    plt.figure(figsize=(desired_width / 80, max_height * scaling_factor / 80))

    plt.subplot(1, 2, 1)
    plt.imshow(np_image1, cmap='gray' if len(np_image1.shape) == 2 else None)
    plt.title("Original")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(np_image2, cmap='gray' if len(np_image2.shape) == 2 else None)
    plt.title("Transformed")
    plt.axis('off')

    plt.show()


def resize_frame(frame, _width, _height):
    # Resize the frame to the new dimensions
    sd_frame = np.array(frame)
    height, width = sd_frame.shape
    # print('channels: ', channels)
    # Initialize the new image array
    new_img_array = np.zeros((_height, _width), dtype=np.uint8)

    # Perform bilinear interpolation
    for i in range(int(_height)):
        for j in range(int(_width)):
            a = sd_frame[i*2, j*2]
            b = sd_frame[i*2, j*2+1]
            c = sd_frame[i*2+1, j*2]
            d = sd_frame[i*2+1, j*2+1]

            summ = a  / 4 + b / 4 + c / 4 + d / 4
            new_img_array[i, j] = summ

    return new_img_array

def resize_video(input_video_path, output_video_path):
    # Load the input video clip
    clip = VideoFileClip(input_video_path,has_mask=True)
    width, height = clip.size[0], clip.size[1]

    # Process each frame of the video
    processed_frames = []
    for frame in clip.mask.iter_frames(dtype="uint8"):
        # print("frame", frame.mask)
        resized_frame = resize_frame(frame, int(width/2), int(height/2))
        processed_frames.append(resized_frame)

    # Create a video clip from the processed frames
    processed_clip = VideoClip(lambda t: processed_frames[int(t * clip.fps)], duration=clip.duration)

    # Write the processed video clip to a file
    processed_clip.write_videofile(output_video_path, fps=clip.fps)

def grayscale_video(input_video_path, output_video_path):
    clip = VideoFileClip(input_video_path)

    # Process each frame of the video
    processed_frames = []
    for frame in clip.iter_frames(dtype="uint8"):
        
        # Resize the frame
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # print("GRAY", grayscale_frame)
        processed_frames.append(grayscale_frame)
    
    # Create a video clip from the processed frames
    processed_clip = VideoClip(lambda t: processed_frames[int(t * clip.fps)], duration=clip.duration)

    # Write the processed video clip to a file
    processed_clip.write_videofile(output_video_path, fps=clip.fps)
    
# def to_grayscale(frame):
# # Convert the frame to grayscale using cv2
#     grayscale_frame = frame.copy()
#     grayscale_frame[:,:,0] = grayscale_frame[:,:,1] = grayscale_frame[:,:,2] = (0.2989*grayscale_frame[:,:,0] + 0.5870*grayscale_frame[:,:,1] + 0.1140*grayscale_frame[:,:,2]).astype('uint8')
#     return grayscale_frame

# def grayscale_video(input_video_path, output_video_path):
# # Load the input video clip
#     clip = VideoFileClip(input_video_path)

#     # Process each frame of the video
#     processed_frames = []
#     for frame in clip.iter_frames():
#         # Convert the frame to grayscale
#         grayscale_frame = to_grayscale(frame)
#         processed_frames.append(grayscale_frame)

#     # Create a video clip from the processed frames
#     processed_clip = VideoClip(lambda t: processed_frames[int(t * clip.fps)], duration=clip.duration)

#     # Write the processed video clip to a file
#     processed_clip.write_videofile(output_video_path, fps=clip.fps)






def convert_to_sd(input_video_path, output_video_path, target_fps):
    # Load the video file
    clip = VideoFileClip(input_video_path)
    print("Original Video Info:")
    print(f"Resolution: {clip.size[0]}x{clip.size[1]}")
    print(f"Frame Rate: {clip.fps}")

    # Check if the video is portrait or landscape
    is_portrait = clip.size[1] > clip.size[0]

    if is_portrait:
        # Rotate the video by 90 degrees if it's portrait
        clip = clip.rotate(90)

    # Trim the video from start_time to end_time

    # Target resolution for SD
    target_width = 640
    target_height = 480

    # Calculate the new dimensions while maintaining the aspect ratio
    original_width, original_height = clip.size
    aspect_ratio = original_width / original_height

    # Calculate the new dimensions while maintaining the aspect ratio
    original_width, original_height = clip.size
    aspect_ratio = original_width / original_height
    
    if original_width / original_height > target_width / target_height:
        # Width is the constraining dimension
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    else:
        # Height is the constraining dimension
        new_height = target_height
        new_width = int(new_height * aspect_ratio)

    # Resize the video
    resized_clip = clip.resize(newsize=(new_width, new_height))

    if clip.fps > target_fps:
        # Set the new fps
        resized_clip = resized_clip.set_fps(target_fps)
    
    # Write the resized video to a file
    temp_path = "temp_resized_vid.mp4"
    resized_clip.write_videofile(temp_path, codec='libx264')

    v = ffmpeg.input(temp_path)
    print (target_height, target_width)
    print (new_height, new_width)
    kwargs = {
        'w':str(target_width), 
        'h':str(target_height), 
        'x':'0' if target_width == new_width else str(int((target_width - new_width) / 2)), 
        'y':'0' if target_height == new_height else str(int((target_height - new_height) / 2)), 
        'color':'black@0'}
    v_pad = ffmpeg.filter(v, filter_name='pad', **kwargs)
    v_pad.output(output_video_path).run()

    os.remove(temp_path)

    return sum(1 for dummy in resized_clip.iter_frames())

if __name__ == "__main__":
    # Example usage
    video_path = get_video_path()
    output_video = 'output_video_sd.mp4'
    convert_to_sd(video_path, output_video, 30)             # 640 * 480
    grayscale_video(output_video, "gray_out.mp4")

    resize_video("gray_out.mp4", "resized_out.mp4")           # 320 * 240
    resize_video("resized_out.mp4", "resized_out2.mp4")     # 160 * 120
    resize_video("resized_out2.mp4", "resized_out3.mp4")    # 80 * 60
    resize_video("resized_out3.mp4", "resized_out4.mp4")    # 40 * 30




