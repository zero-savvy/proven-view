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
            print(packet.stream.codec_context)
            data = packet
            print("size: ", data.size)
            # Save each frame packet as a raw file
            with open(f"{output_folder}/frame_{frame_index}.hex", 'w') as f:
                for i in range(0, data.size, 32):  # 32 bytes == 256 bits
                    chunk = data[i:i+32]
                    hex_chunk = chunk.hex()  # Convert bytes to hex
                    f.write(hex_chunk + "\n")  # Write the hex chunk as a line
                
                # f.write(packet)
                # frame_index += 1
        frame_index += 1
    
    print(f"Extracted {frame_index} frames as raw data.")

# Example usage:
video_path = '/home/parisa/Desktop/video-proof/proven_view/proven-view/samples/security_camera.mp4'
output_folder = 'output_frames'
save_frames_as_raw(video_path, output_folder)