import os
import json

import av
import ffmpeg
import math

from utils.video import get_video_path
from utils.calc_merkle_path import calc_merkle_path



def get_fps(input_path):
    """
    Get the frames per second (fps) of a video.
    """
    probe = ffmpeg.probe(input_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    fps = eval(video_stream['avg_frame_rate'])  # avg_frame_rate is in format "num/den"
    return fps

def time_to_frame_index(time_str, fps):
    """
    Convert time (hh:mm:ss or seconds) to a frame index based on the fps.
    
    Args:
    - time_str (str or float): Time in 'hh:mm:ss' format or as a float representing seconds.
    - fps (float): Frames per second of the video.
    
    Returns:
    - int: The frame index.
    """
    # Convert time_str to total seconds if in hh:mm:ss format
    if isinstance(time_str, str):
        h, m, s = map(float, time_str.split(':'))
        total_seconds = h * 3600 + m * 60 + s
    else:
        total_seconds = float(time_str)
    
    # Calculate frame index
    frame_index = math.floor(total_seconds * fps) - 1
    return int(frame_index)

def trim_video(input_path, output_path, start_frame_index, end_frame_index):
    """
    Trim a video without re-encoding, preserving frame types (I, P, B).

    Args:
    - input_path (str): Path to the input video file.
    - output_path (str): Path to save the trimmed output video.
    - start_time (str): Start time in 'hh:mm:ss' format or seconds.
    - end_time (str): End time in 'hh:mm:ss' format or seconds.
    """

    # Use ffmpeg to trim the video between start_time and end_time without re-encoding
    # ffmpeg.input(input_path, ss=start_time, to=end_time).output(output_path, c='copy').run()

    # Step #0: reading each frame data
    container = av.open(input_path)
    
    # Create an index for naming the frames
    # prev_hash_value = "0x00"
    # frames_hash_values = []
    # Loop through packets (encoded data)
    frame_index = -1
    write_content = {"witness": []}
    for packet in container.demux():
        # Check if the packet belongs to a video stream
        if packet.stream.type == 'video':
            frame_index += 1
            if frame_index < start_frame_index:
                continue
            if frame_index > end_frame_index:
                break

            binary_data = bytes(packet)

            for i in range(0, len(binary_data), 31):  # 32 bytes == 256 bits
                chunk = binary_data[i:i+31]
                hex_chunk = chunk.hex()  # Convert bytes to hex
                write_content["witness"].append(hex_chunk)
    with open(f"{output_path}/witness_data.json", 'w') as f:
        json.dump(write_content, f, indent=2)

# Example usage
input_video = get_video_path()
output_video = "output_trimmed"
start_time = "00:00:05"  # Start time (1 minute into the video)
end_time = "00:00:10"    # End time (2 minutes 30 seconds into the video)
fps = get_fps(input_video)
start_frame_index = time_to_frame_index(start_time, fps)
end_frame_index = time_to_frame_index(end_time, fps)
print(fps)
print(start_frame_index)
print(end_frame_index)
output_folder = 'trimmed_frames'
os.makedirs(output_folder, exist_ok=True) 
trim_video(input_video, output_folder, start_frame_index, end_frame_index)
# get the Merkle tree file path
print("select Merkle tree file ...")
merkle_file = get_video_path()
prev_hash, leaf_start, merkle_path_start, positions_start = calc_merkle_path(merkle_file, start_frame_index)
_, leaf_end, merkle_path_end, positions_end = calc_merkle_path(merkle_file, end_frame_index)

