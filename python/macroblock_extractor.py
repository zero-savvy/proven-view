import subprocess
import json

def extract_macroblocks(video_path, output_path):
    """
    Extracts raw macroblocks from an H.264 video file by reading the bitstream as raw bytes.
    
    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path to save the extracted macroblocks.
    """
    # Step 1: Use ffmpeg to extract the raw H.264 bitstream (Annex B format)
    raw_stream_path = "raw.h264"
    subprocess.run([
        "ffmpeg", "-i", video_path, "-c:v", "copy", "-bsf:v", "h264_mp4toannexb", 
        "-f", "h264", raw_stream_path
    ], check=True)
    
    # Step 2: Open the raw H.264 stream and parse it as raw bytes
    with open(raw_stream_path, "rb") as f:
        bitstream = f.read()  # Read the entire raw bitstream as binary data
        
        # Step 3: Extract NAL units
        nal_units = extract_nal_units(bitstream)

        # Step 4: Extract macroblocks from NAL units
        macroblocks = []
        for nal in nal_units:
            macroblocks.extend(extract_macroblocks_from_nal(nal))

        # Step 5: Save macroblock data to the output file
    with open(output_path, "w") as out_file:
        json.dump(macroblocks, out_file, indent=4)



def extract_nal_units(bitstream):
    """
    Extracts NAL units from the raw H.264 bitstream.
    
    Args:
        bitstream (bytes): The raw H.264 bitstream data.

    Returns:
        list: A list of NAL unit byte arrays.
    """
    nal_units = []
    start_code = b'\x00\x00\x01'  # NAL start code (3 bytes)
    start_code_4bytes = b'\x00\x00\x00\x01'  # Alternative 4-byte start code

    i = 0
    while i < len(bitstream):
        # Find the NAL start code (either 3 or 4 bytes)
        if bitstream[i:i+3] == start_code:
            start = i + 3
            i = start
        elif bitstream[i:i+4] == start_code_4bytes:
            start = i + 4
            i = start
        else:
            i += 1
            continue
        
        # Find the end of the NAL unit (next start code)
        end1 = bitstream.find(start_code, start)
        end2 = bitstream.find(start_code_4bytes, start)
        if end1 == -1:
            end1 = len(bitstream)
        if end2 == -1:
            end2 = len(bitstream)
        end = min(end1, end2)
        
        # Append the NAL unit
        nal_units.append(bitstream[start:end])

    return nal_units


def extract_macroblocks_from_nal(nal_data):
    """
    Extracts raw macroblocks from a single NAL unit.
    
    Args:
        nal_data (bytes): A NAL unit containing slice data.

    Returns:
        list: A list of macroblock data (raw bytes).
    """
    macroblocks = []
    
    # For simplicity, let's assume that each NAL unit corresponds to a slice.
    # We need to split the slice data into macroblocks (simplified approach).
    
    # Here we're just extracting chunks of data as macroblocks
    # For simplicity, we take every 16 bytes as one macroblock (this is just an example)
    # chunk_size = 16  # Example: a macroblock might be around 16 bytes (simplified)
    
    mb = ''
    for i in range(0, len(nal_data)):
        if nal_data[i] == 1:
            macroblocks.append(mb)
            mb = ''
        mb += hex(nal_data[i])[2:]
    
    if len(mb) > 0:
        macroblocks.append(mb)
    return macroblocks
    # return [nal_data.hex()]


# Example usage
extract_macroblocks("/home/shahriar/Projects/zero-savvy/proven-view/samples/security-camera.mp4", "macroblocks.json")
