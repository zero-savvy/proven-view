import os
import cv2
import json
import numpy as np
from PIL import Image
import ffmpeg
import tkinter as tk
from tkinter import filedialog


# def get_video_path():
#     root = tk.Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename()
#     return file_path

# image_path = get_video_path()
# input_file = ffmpeg.input(image_path)
# output_file = ffmpeg.output(input_file.trim(start_frame=80, end_frame=90), 'output.mp4')
# ffmpeg.run(output_file)
# vidcap = cv2.VideoCapture('output.mp4')
# success,image = vidcap.read()
# count = 0
# while success:
#   cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
#   success,image = vidcap.read()
#   print('Read a new frame: ', success)
#   count += 1


# Function to extract frames from a video until reaching the desired frame count
# def extract_frames(video_file):
#     cap = cv2.VideoCapture(video_file)
    
#     frame_rate = 1  # Desired frame rate (1 frame every 0.5 seconds)
#     frame_count = 0
    
#     # Get the video file's name without extension
#     video_name = os.path.splitext(os.path.basename(video_file))[0]
    
    # Create an output folder with a name corresponding to the video
    # output_directory = f"{video_name}_frames"
    # os.makedirs(output_directory, exist_ok=True)
    
    # while True:
    #     ret, frame = cap.read()
        
    #     if not ret:
    #         break
        
    #     frame_count += 1
        
    #     # Only extract frames at the desired frame rate
    #     if frame_count % int(cap.get(5) / frame_rate) == 0:
    #         output_file = f"{output_directory}/frame_{frame_count}.jpg"
    #         cv2.imwrite(output_file, frame)
    #         print(f"Frame {frame_count} has been extracted and saved as {output_file}")
    
    # cap.release()
    # cv2.destroyAllWindows()

def compress_image(image_path):
    with Image.open(image_path) as image:
        return compress(image)

def compress(image_in):
    array_in = np.array(image_in).tolist()
    output_array = []
    # print(len(array_in), len(array_in[0]), len(array_in[0][0]))

    for i in range(0, len(array_in)):
        row = []
        hexValue = ''
        for j in range(0, len(array_in[i])):
            if np.isscalar(array_in[i][j]):
                hexValue = hex(int(array_in[i][j]))[2:].zfill(6) + hexValue
            else:
                for k in range(0, 3):
                    hexValue = hex(int(array_in[i][j][k]))[2:].zfill(2) + hexValue
            if j % 10 == 9:
                row.append("0x" + hexValue)
                hexValue = ''
        output_array.append(row)
    return output_array

# ////////////////////////////////////////////////////////////////////
def extract_frames(video_path, start_frame, end_frame, output_path):
    
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    # Get total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Check if the start and end frames are within the total number of frames
    if start_frame >= total_frames or end_frame >= total_frames:
        print("Start or end frame exceeds total number of frames.")
        return
    
    if not os.path.exists(output_path):
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
    video_file = r"SampleVideo_1280x720_1mb.mp4"  # Replace with your video's name
    print('start')
    end_frame = 102
    start_frame = 100
    output_path = "out_frames"
    extract_frames(video_file, start_frame, end_frame, output_path)
    compressed_out = []
    current_directory = os.getcwd()
    # Crop the image and save it
    for i in range(end_frame-start_frame):
        relative_image_path = output_path + f"/frame_{i}.jpg"
        image_path = os.path.join(current_directory, relative_image_path)
        with Image.open(image_path) as image:
            compressed_original_image = compress(image)
            compressed_out.append(compressed_original_image)
        # compressed_original_image = compress_image(output_path)
    out = {
        "original": compressed_out,
    }
    print("Image compressed successfully.")
    with open(f"{output_path}/output_file.json", 'w') as fp:
        json.dump(out, fp, indent=4)

