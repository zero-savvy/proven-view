# This code converts videos with every resolution to SD, and resize the video with your target fps.
import os
import json

import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
from utils.poseidon import frames_hash
from utils.merkle import build_merkle_tree
from utils.video import get_video_path, convert_set_frames
from utils.video_edit import compress_frames


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


if __name__ == "__main__":
    # Example usage
    video_path = get_video_path()
    output_video = 'fixed_frame_rate.mp4'

    # Step 1
    convert_set_frames(video_path, output_video, 1) 
    
    # Step 2
    out = compress_frames(output_video)

    # Step 3
    frames_hash_values = frames_hash(out)
    with open("outputs.json", 'w') as fp:
        json.dump(frames_hash_values, fp, indent=4)

    # Step 4
    merkle_tree = build_merkle_tree(frames_hash_values)
    print("Merkle root of the commited video:", merkle_tree[0][0])

    merkle_file = 'tree.json'
    with open(merkle_file, 'w') as mkf:
        json.dump(merkle_tree, mkf, indent=4)

    # Step 5
    # sign_and_commit(merkle_tree[0][0])




