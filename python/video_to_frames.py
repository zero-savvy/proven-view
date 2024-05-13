# This code converts video file to its frames and save the selected range of them (start-end).
import os
import shutil
import json

import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image

from convert_to_sd import convert_to_sd



def get_video_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

# def compress_image(image_path):
#     with Image.open(image_path) as image:
#         return compress(image)

def pixel_to_array(image_in):
    array_in = np.array(image_in).tolist()
    output_array = []
    # print(len(array_in), len(array_in[0]), len(array_in[0][0]))

    for i in range(0, len(array_in)):
        row = []
        hexValue = ''
        for j in range(0, len(array_in[i])):
            # if np.isscalar(array_in[i][j]):
            #     hexValue = hex(int(array_in[i][j]))[2:].zfill(6) + hexValue
            # else:
            #     for k in range(0, 3):
            #         hexValue = hex(int(array_in[i][j][k]))[2:].zfill(2) + hexValue
            # if j % 2 == 1:
            row.append(["0x" + hex(int(array_in[i][j][k]))[2:].zfill(2) for k in range(0, 3)])
        output_array.append(row)
    return output_array

# ////////////////////////////////////////////////////////////////////
def extract_frames(video_path, start_frame, end_frame, output_path):
    
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    # Get total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print (start_frame, total_frames, end_frame, total_frames)
    
    # Check if the start and end frames are within the total number of frames
    if start_frame > total_frames or end_frame > total_frames:
        print("Start or end frame exceeds total number of frames.")
        return
    
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    
    os.makedirs(output_path)

    # Set the start frame
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    # Loop through the frames and extract them
    frame_count = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Check if end frame reached
        if frame_count > end_frame - start_frame:
            break
        
        # Save the frame
        # frame_output_path = f"{output_path}/frame_{frame_count}.jpg"
        frame_output_path = os.path.join(output_path, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_output_path, frame)
        frame_count += 1
        
    
    # Release the video capture object
    video_capture.release()

if __name__ == "__main__":
    # video_file = r"SampleVideo_1280x720_1mb.mp4"  # Replace with your video's name
    video_path = get_video_path()
    print('start ...')
    start_time = int(input("Enter start frame (this frame will include): ") or "0")
    end_time = int(input("Enter end frame (this frame will include): ") or "1")
    resolution = int(input("Proving Resolution: 1) SD, 2) HD, 3) FHD: ") or "1")
    height = 480 if resolution == 1 else (720 if resolution == 1 else 1080)
    output_path = "out_frames"
    output_video = 'resized_video.mp4'
    total_frames = convert_to_sd(video_path, output_video, start_time, end_time, 30)
    extract_frames(output_video, 0, total_frames, output_path)
    compressed_out = []
    current_directory = os.getcwd()
    
    # Crop the image and save it
    general_json = {
        "height": height,
        "frames": total_frames,
    }
    with open(f"{output_path}/general.json", 'w') as fp:
        json.dump(general_json, fp, indent=4)

    for i in range(total_frames):
        relative_image_path = output_path + f"/frame_{i}.jpg"
        relative_json_path = output_path + f"/frame_{i}.json"
        image_path = os.path.join(current_directory, relative_image_path)
        with Image.open(image_path) as image:
            frame_data = {
                "orig": pixel_to_array(image),
            }
            with open(relative_json_path, 'w') as fp:
                json.dump(frame_data, fp, indent=4)
            os.unlink(image_path)
        # compressed_original_image = compress_image(output_path)
    print("Generated inputs for Nova successfully at directory: ./" + output_path + "/")
    
