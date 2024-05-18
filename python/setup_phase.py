# This code converts videos with every resolution to SD, and resize the video with your target fps.
import os
import json

import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
from utils.poseidon import frames_hash
from utils.merkle import build_merkle_tree
from utils.convert_to_sd import convert_to_sd
from utils.video_edit import grayscale_video, resize_video
from utils.json_helper import compress

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


if __name__ == "__main__":
    # Example usage
    video_path = get_video_path()
    output_video = 'output_video_sd.mp4'

    # Step 1
    convert_to_sd(video_path, output_video, 30)             # 640 * 480
    
    # Step 2
    tmp, fps = grayscale_video(output_video, "gray_out.mp4")
    frames = resize_video(tmp, "resized_out.mp4", fps)
    out = compress(frames)

    # Step 3
    frames_hash_values = frames_hash(out)
    with open("outputs.json", 'w') as fp:
        json.dump(frames_hash_values, fp, indent=4)

    # Step 4
    merkle_tree = build_merkle_tree(frames_hash_values)
    print(merkle_tree[0][0])

    # Step 5
    # sign_and_commit(merkle_tree[0][0])




