import os
import shutil

import cv2
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip, ImageSequenceClip


def resize_frame(frame):
    # Resize the frame to the new dimensions
    # sd_frame = np.array(frame)
    # height, width = sd_frame.shape
    # print('channels: ', channels)
    # Initialize the new image array
    k = 16  # from SD --to--> 30x40 resolution
    _width, _height = int(len(frame[0])/k), int(len(frame)/k)
    new_img_array = np.zeros((_height, _width), dtype=np.uint8)

    # Perform bilinear interpolation
    for i in range(int(_height)):
        for j in range(int(_width)):
            summ = 0
            for m in range (k):
                for n in range (k):
                    summ += frame[i*k+n, j*k+m] / (k * k)
            new_img_array[i, j] = summ

    return new_img_array

def resize_video(np_array, output_video_path, fps):
    
    # target_width = 40
    # target_height = 30

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


def trim(input_video_path, start_time, end_time, output_path, output_video_path):

    # Load the input video clip
    clip = VideoFileClip(input_video_path)

    total_frames = clip.iter_frames(dtype="uint8").count()
    start_frame = int(start_time * clip.fps)
    end_frame = max(int(end_time * clip.fps), total_frames)

    if start_frame > total_frames:
        print("Start frame exceeds total number of frames.")
        return
    
    # Process each frame of the video
    processed_frames = []
    for i, frame in enumerate(clip.iter_frames(dtype="uint8")[start_frame, end_time]):
        image = Image.fromarray(frame)
        processed_frames.append(image)

        frame_output_path = os.path.join(output_path, f"frame_{i}.jpg")
        cv2.imwrite(frame_output_path, frame)

    # Create a video from the processed frames
    video_clip = ImageSequenceClip([frame for frame in processed_frames], fps=clip.fps)

    # Write the video to a file
    video_clip.write_videofile(output_video_path, codec='libx264')   # Create a video clip from the processed frames

    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    
    os.makedirs(output_path)

    
    for i, frame in enumerate(data[start_frame, end_frame]):
        

    
    return tree
