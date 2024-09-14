# This code converts video file to its frames and save the selected range of them (start-end).
import os
import json

import tkinter as tk
from tkinter import filedialog

from utils.calc_merkle_path import calc_merkle_path
from utils.video_edit import trim


def get_video_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


if __name__ == "__main__":
    
    video_path = get_video_path()
    print('start ...')
    start_time = int(input("Enter start frame (this frame will include): ") or "0")
    end_time = int(input("Enter end frame (this frame will include): ") or "1")
    
    output_path = "out_frames"
    trimmed_video = 'trimmed_video.mp4'
    # sd_video = 'sd_video.mp4'
    # gray_video = 'gray_video.mp4'
    squeezed_video = 'squeezed_video.mp4'

    # Step 1
    # convert_to_sd(video_path, sd_video, 30)

    # Trim the video
    start_frame, end_frame, total_frames =  trim(video_path, start_time, end_time, output_path, trimmed_video)
    
    # # Step 2
    # tmp, fps = grayscale_video(trimmed_video, gray_video)
    # frames = resize_video(tmp, squeezed_video, fps)
    # out = compress(frames)

    # # Step 3
    # frames_hash_values = frames_hash(out)
    # with open("outputs.json", 'w') as fp:
    #     json.dump(frames_hash_values, fp, indent=4)


    # compressed_out = []
    current_directory = os.getcwd()
    
    # Create inputs for Nova prover
    merkle_file = 'tree.json'
    prev_hash, leaf_start, merkle_path_start, positions_start = calc_merkle_path(merkle_file, start_frame)
    _, leaf_end, merkle_path_end, positions_end = calc_merkle_path(merkle_file, end_frame)
    general_json = {
        # "height": height,
        "frames": total_frames,
        "prev_hash": [
            int(prev_hash[48:], 16),
            int(prev_hash[32:48], 16),
            int(prev_hash[16:32], 16),
            int(prev_hash[:16], 16),
            ],
    }

    path_json = {
        "levels": len(merkle_path_start),
        "path_elements_start": merkle_path_start,
        "path_indices_start": positions_start,
        "leaf_start": [
            int(leaf_start[48:], 16),
            int(leaf_start[32:48], 16),
            int(leaf_start[16:32], 16),
            int(leaf_start[:16], 16),
            ],
        "path_elements_end": merkle_path_end,
        "path_indices_end": positions_end,
        "leaf_end": [
            int(leaf_end[48:], 16),
            int(leaf_end[32:48], 16),
            int(leaf_end[16:32], 16),
            int(leaf_end[:16], 16),
            ],
    }
    with open(f"{output_path}/general.json", 'w') as fp:
        json.dump(general_json, fp, indent=4)

    with open(f"{output_path}/path.json", 'w') as fp:
        json.dump(path_json, fp, indent=4)

    # for i in range(total_frames):
    #     relative_image_path = output_path + f"/frame_{i}.jpg"
    #     relative_json_path = output_path + f"/frame_{i}.json"
    #     image_path = os.path.join(current_directory, relative_image_path)
            
        # compressed_original_image = compress_image(output_path)
    print("Generated inputs for Nova successfully at directory: ./" + output_path + "/")
    
