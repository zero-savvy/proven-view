# import av

# def save_frames_as_raw(video_path, output_folder):
#     # Open the video file
#     container = av.open(video_path)
    
#     # Create an index for naming the frames
#     frame_index = 0
    
#     # Loop through packets (encoded data)
#     for packet in container.demux():
#         # Check if the packet belongs to a video stream
#         if packet.stream.type == 'video':
#             for frame in packet.decode():
#                 data = frame
#                 print(data)
#                 # Save each frame packet as a raw file
#                 with open(f"{output_folder}/frame_{frame_index}.hex", 'w') as f:
#                     for i in range(0, data.__len__, 32):  # 32 bytes == 256 bits
#                         chunk = data[i:i+32]
#                         hex_chunk = chunk.hex()  # Convert bytes to hex
#                         f.write(hex_chunk + "\n")  # Write the hex chunk as a line
                
#                 # f.write(packet)
#                 # frame_index += 1
#         frame_index += 1
    
#     print(f"Extracted {frame_index} frames as raw data.")

# # Example usage:
# video_path = '/home/parisa/Desktop/video-proof/proven_view/proven-view/samples/security_camera.mp4'
# output_folder = 'output_frames'
# save_frames_as_raw(video_path, output_folder)

import os
import json
import av


def save_frames_as_raw(video_path, output_folder):
    # Open the video file
    container = av.open(video_path)
    
    # Create an index for naming the frames
    frame_index = 0
    
    # Loop through packets (encoded data)
    for packet in container.demux():
        # Check if the packet belongs to a video stream
        if packet.stream.type == 'video':
            # Save each frame packet as a raw file
            with open(f"{output_folder}/frame_{frame_index}.json", 'w') as f:
                binary_data = bytes(packet)
                write_content = {"witness": []}
                for i in range(0, len(binary_data), 31):  # 32 bytes == 256 bits
                    chunk = binary_data[i:i+31]
                    hex_chunk = chunk.hex()  # Convert bytes to hex
                    write_content["witness"].append(hex_chunk)
                json.dump(write_content, f, indent=2)
                frame_index += 1
    
    print(f"Extracted {frame_index} frames as raw data.")


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '../samples', 'security_camera.mp4')
output_folder = 'output_frames'
save_frames_as_raw(file_path, output_folder)