# This code converts videos with every resolution to SD, and resize the video with your target fps.
import os
import json

import tkinter as tk
from tkinter import filedialog
import av

import matplotlib.pyplot as plt
from utils.poseidon import frames_hash, integrity_frames_hash, frame_hashes
from utils.merkle import build_merkle_tree
from utils.video import get_video_path, convert_set_frames
from utils.video_edit import compress_frames


if __name__ == "__main__":
    # 
    video_path = get_video_path()

    # Step #0: reading each frame data
    container = av.open(video_path)
    
    # Create an index for naming the frames
    prev_hash_value = "0x00"
    frames_data = []
    # Loop through packets (encoded data)
    for packet in container.demux():
        # Check if the packet belongs to a video stream
        if packet.stream.type == 'video':

            binary_data = bytes(packet)
            frame_data = []
            for i in range(0, len(binary_data), 31):  # 31 bytes == 248 bits
                chunk = binary_data[i:i+31]
                hex_chunk = chunk.hex()  # Convert bytes to hex
                frame_data.append("0x" + str(hex_chunk))  # Save the values in string form
            prev_hash_value = integrity_frames_hash(prev_hash_value, frame_data)
            frames_data.append(frame_data)
    
    # Step #1: writing the intergrity(chained) hash in the file.
    integrity_file = 'integrity_hash.json'
    with open(integrity_file, 'w') as mkf:
        json.dump(prev_hash_value, mkf, indent=4)
    #Step #2: Calculating Merkle tree leaves and writing them in file
    frames_hash_values = frame_hashes(frames_data)
    with open("outputs.json", 'w') as fp:
        json.dump(frames_hash_values, fp, indent=4)

    # Step #3: Building Merkle tree
    merkle_tree = build_merkle_tree(frames_hash_values)
    print("Merkle root of the commited video:", merkle_tree[0][0])

    # Step #4: Writing Merkle Root Hash in file
    merkle_file = 'tree.json'
    with open(merkle_file, 'w') as mkf:
        json.dump(prev_hash_value, mkf, indent=4)

    # Step #5
    # sign_and_commit(merkle_tree[0][0])




