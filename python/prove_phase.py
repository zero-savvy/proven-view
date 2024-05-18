# This code converts video file to its frames and save the selected range of them (start-end).
import os
import shutil
import json

import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image

from utils.calc_merkle_path import calc_merkle_path
from utils.poseidon import frames_hash
from utils.convert_to_sd import convert_to_sd
from utils.video_edit import grayscale_video, resize_video, trim
from utils.json_helper import compress


def get_video_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def pixel_to_array(image_in):
    array_in = np.array(image_in).tolist()
    output_array = []

    for i in range(0, len(array_in)):
        row = []
        hexValue = ''
        for j in range(0, len(array_in[i])):
            row.append(["0x" + hex(int(array_in[i][j][k]))[2:].zfill(2) for k in range(0, 3)])
        output_array.append(row)
    return output_array


if __name__ == "__main__":
    
    video_path = get_video_path()
    print('start ...')
    start_time = int(input("Enter start frame (this frame will include): ") or "0")
    end_time = int(input("Enter end frame (this frame will include): ") or "1")
    
    output_path = "out_frames"
    trimmed_video = 'trimmed_video.mp4'
    sd_video = 'sd_video.mp4'
    gray_video = 'gray_video.mp4'
    squeezed_video = 'squeezed_video.mp4'

    # Step 1
    convert_to_sd(video_path, sd_video, 30)

    # Trim the video
    start_frame, end_frame, total_frames =  trim(sd_video, start_time, end_time, output_path, trimmed_video)
    
    # Step 2
    tmp, fps = grayscale_video(trimmed_video, gray_video)
    frames = resize_video(tmp, squeezed_video, fps)
    out = compress(frames)

    # Step 3
    frames_hash_values = frames_hash(out)
    with open("outputs.json", 'w') as fp:
        json.dump(frames_hash_values, fp, indent=4)


    compressed_out = []
    current_directory = os.getcwd()
    
    # Create inputs for Nova prover
    merkle_file = 'tree.json'
    general_json = {
        # "height": height,
        "frames": total_frames,
        "path_start": calc_merkle_path(merkle_file, start_frame),
        "path_end": calc_merkle_path(merkle_file, end_frame),
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
    
