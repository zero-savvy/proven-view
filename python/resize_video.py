# This code converts videos with every resolution to SD, and resize the video with your target fps.
import os
import json

import tkinter as tk
from tkinter import filedialog

import numpy as np
import ffmpeg
import cv2
from moviepy.editor import VideoFileClip, VideoClip, ImageSequenceClip
import moviepy
from PIL import Image

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


def compress(array_in):
    
    output_array = []
    # print(len(array_in), len(array_in[0]), len(array_in[0][0]))
    for frame in array_in:
        frame_array = []
        for i in range(0, len(frame)):
            hexValue = ''
            for j in range(0, len(frame[i])):
                hexValue = hex(int(frame[i][j]))[2:].zfill(2) + hexValue
            frame_array.append(hexValue)
        output_array.append(frame_array)
    return output_array


def resize_frame(frame):
    # Resize the frame to the new dimensions
    # sd_frame = np.array(frame)
    # height, width = sd_frame.shape
    # print('channels: ', channels)
    # Initialize the new image array
    k = 16
    _width, _height = int(len(frame[0])/k), int(len(frame)/k)
    new_img_array = np.zeros((_height, _width), dtype=np.uint8)

    # Perform bilinear interpolation
    for i in range(int(_height)):
        for j in range(int(_width)):
            summ = 0
            for m in range (k):
                for n in range (k):
                    summ += frame[i*k+n, j*k+m] / (k * k)
                    # a = frame[i*4, j*4]
                    # b = frame[i*4, j*4+1]
                    # c = frame[i*4+1, j*4]
                    # d = frame[i*4+1, j*4+1]
            new_img_array[i, j] = summ

    return new_img_array

def resize_video(np_array, output_video_path, fps):
    
    target_width = 40
    target_height = 30

    # Process each frame of the video
    processed_frames = []
    video_frames = []
    print("VIDEO SIZE:", len(np_array), len(np_array[0]), len(np_array[0][0]))
    for i, frame in enumerate(np_array):
        # print("frame", frame.mask)
        # if i % 100 == 0:
        #     print(i)
        resized_frame = frame
        # while len(resized_frame) > target_height:
            # print(len(resized_frame))
        resized_frame = resize_frame(resized_frame)
        processed_frames.append(resized_frame)
    
        rgb_frame = np.stack((resized_frame,)*3, axis=-1)
        video_frames.append(rgb_frame)

    # Create a video from the processed frames
    video_clip = ImageSequenceClip([frame for frame in video_frames], fps=fps)

    # Write the video to a file
    video_clip.write_videofile(output_video_path, codec='libx264')   # Create a video clip from the processed frames

    return processed_frames


def grayscale_video(input_video_path, output_video_path):
# Load the input video clip
    clip = VideoFileClip(input_video_path)

    # Process each frame of the video
    processed_frames = []
    gray_array = []
    for frame in clip.iter_frames(dtype="uint8"):
        # Convert the frame to grayscale
        image = Image.fromarray(frame)
        grayscale_image = image.convert('L')
        # grayscale_frame = to_grayscale(frame)
        grayscale_array = np.array(grayscale_image)
        gray_array.append(grayscale_array)
        rgb_frame = np.stack((grayscale_array,)*3, axis=-1)
        processed_frames.append(rgb_frame)

    # Create a video from the processed frames
    video_clip = ImageSequenceClip([frame for frame in processed_frames], fps=clip.fps)

    # Write the video to a file
    video_clip.write_videofile(output_video_path, codec='libx264')   # Create a video clip from the processed frames

    return gray_array, clip.fps


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
    tmp, fps = grayscale_video(output_video, "gray_out.mp4")

    frames = resize_video(tmp, "resized_out.mp4", fps)
    out = compress(frames)
    with open("outputs.json", 'w') as fp:
        json.dump(out, fp, indent=4)




