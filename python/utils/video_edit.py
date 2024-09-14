import os
import shutil
import json

import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip, ImageSequenceClip


def resize_video(np_array, output_video_path, fps):
    
    # target_width = 40
    # target_height = 30

    # Process each frame of the video
    processed_frames = []
    video_frames = []
    print("VIDEO SIZE:", len(np_array), len(np_array[0]), len(np_array[0][0]))
    for i, frame in enumerate(np_array):
        resized_frame = frame
        resized_frame = resize_frame(resized_frame)
        processed_frames.append(resized_frame)
    
        rgb_frame = np.stack((resized_frame,)*3, axis=-1)
        video_frames.append(rgb_frame)

    # Create a video from the processed frames
    video_clip = ImageSequenceClip([frame for frame in video_frames], fps=fps)

    # Write the video to a file
    video_clip.write_videofile(output_video_path, codec='libx264')   # Create a video clip from the processed frames

    return processed_frames


def _compress_frames(clip, start: int = None, end: int = None):
    # Process each frame of the video
    # processed_frames = []
    output_array = []
    for i, frame in enumerate(clip.iter_frames(dtype="uint8")):

        if start and end:
            if i < start or i > end:
                continue
        
        image = Image.fromarray(frame).convert('L')

        original_frame = np.array(image).tolist()
        
        frame_array = []

        for i in range(0, len(original_frame)):
            row = []
            hexValue = ''
            for j in range(0, len(original_frame[i])):
                # if np.isscalar(original_frame[i][j]):  # The frame is Grayscale, i.e. no RGB value.
                hexValue = hex(int(original_frame[i][j]))[2:].zfill(6) + hexValue
                # else:
                #     for k in range(0, 3):
                #         hexValue = hex(int(original_frame[i][j][k]))[2:].zfill(2) + hexValue
                if j % 10 == 9:
                    row.append("0x" + hexValue)
                    hexValue = ''
            frame_array.append(row)
        
        output_array.append(frame_array)

    return output_array



def compress_frames(input_video_path):
    # Load the input video clip
    clip = VideoFileClip(input_video_path)
    return _compress_frames(clip)


def pixel_to_array(image_in):
    array_in = np.array(image_in).tolist()
    output_array = []

    for i in range(0, len(array_in)):
        row = []
        hexValue = ''
        for j in range(0, len(array_in[i])):
            row.append(hex(int(array_in[i][j])))
        output_array.append(row)
    return output_array


def trim(input_video_path, start_time, end_time, output_path, output_video_path):

    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    # Load the input video clip
    clip = VideoFileClip(input_video_path)

    total_frames = 0
    # We use this method instead of List.count to prevent large memory allocation!
    for i in clip.iter_frames(dtype="uint8"):
        total_frames += 1

    start_frame = int(start_time * clip.fps)
    end_frame = min(int(end_time * clip.fps), total_frames)
    
    # Process each frame of the video
    # processed_frames = []
    # original_frames = []

    print (f"START FRAME: {start_frame}, END FRAME: {end_frame}")

    compressed_frames = _compress_frames(clip, start_frame, end_frame)

    for i, cf in enumerate(compressed_frames):

        frame_output_path = os.path.join(output_path, f"frame_{i}.json")
        # cv2.imwrite(frame_output_path, frame)

        with open(frame_output_path, 'w') as fp:
            json.dump(cf, fp, indent=4)
        # os.unlink(image_path)


    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip, ffmpeg_movie_from_frames
    ffmpeg_extract_subclip(input_video_path, start_time, end_time, targetname="trimmed_video.mp4")

    # # Create a video from the processed frames
    # video_clip = ImageSequenceClip([frame for frame in compressed_frames], fps=clip.fps)

    # # Write the video to a file
    # video_clip.write_videofile(output_video_path, codec='libx264')   # Create a video clip from the processed frames

    return start_frame, end_frame, end_frame - start_frame + 1

