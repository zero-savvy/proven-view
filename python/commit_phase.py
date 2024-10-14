# This code calculate the hash of the input video, generate Merkle tree, and Merkle root.
import os
import json

import av
from tqdm import tqdm

from utils.poseidon import integrity_frames_hash
from utils.merkle import build_merkle_tree
from utils.video import get_video_path


if __name__ == "__main__":
    # 
    video_path = get_video_path()

    # Step #0: reading each frame data
    container = av.open(video_path)
    
    # Create an index for naming the frames
    prev_hash_value = "0x00"
    frames_hash_values = []
    # Loop through packets (encoded data)
    for packet in tqdm(container.demux()):
        # Check if the packet belongs to a video stream
        if packet.stream.type == 'video':

            binary_data = bytes(packet)
            frame_data = []
            for i in range(0, len(binary_data), 31):  # 31 bytes == 248 bits
                chunk = binary_data[i:i+31]
                hex_chunk = chunk.hex()  # Convert bytes to hex
                frame_data.append("0x" + str(hex_chunk))  # Save the values in string form
            prev_hash_value = integrity_frames_hash(prev_hash_value, frame_data)
            frames_hash_values.append(prev_hash_value)  
    
    # Step #1: writing the intergrity(chained) hash in the file.
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True) 
    integrity_file = '/integrity_hash.json'
    with open(output_folder+integrity_file, 'w') as mkf:
        json.dump(prev_hash_value, mkf, indent=4)
    #Step #2: Calculating Merkle tree leaves and writing them in file
    # frames_hash_values = frame_hashes(frames_data)
    
    # Step #3: Building Merkle tree
    merkle_tree = build_merkle_tree(frames_hash_values)
    print("Merkle root of the commited video:", merkle_tree[0][0])

    with open(output_folder+"/Merkle_tree.json", 'w') as fp:
        json.dump(merkle_tree, fp, indent=4)


    # Step #4: Writing Merkle Root Hash in file
    merkle_file = '/root.json'
    with open(output_folder+merkle_file, 'w') as mkf:
        json.dump(merkle_tree[0][0], mkf, indent=4)

    # Step #5
    # sign_and_commit(merkle_tree[0][0])




