import subprocess
import json
import os
from tqdm import tqdm


def poseidon(num1: str, num2: str):
    input_data = {
        "in1": num1,
        "in2": num2
    }
    
    # Write the input data to a JSON file
    input_file = "poseidon-input.json"
    with open(input_file, 'w') as f:
        json.dump(input_data, f)
    
    try:
        result = subprocess.run(['./../circuits/poseidon_cpp/poseidon', 
                                 'poseidon-input.json', 'witness.wtns'], 
                                 capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        output_number = int(output)
        return hex(output_number)
    
    except subprocess.CalledProcessError as e:
        print(f" Witness generator failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
        return None
    
    finally:
        # Remove the input file
        if os.path.exists(input_file):
            os.remove(input_file)
        if os.path.exists('witness.wtns'):
            os.remove('witness.wtns')


def frames_hash(frames: list):
    frames_hash_values = []
    hash_val = "0x00"
    for i in tqdm(range(len(frames))):
        for y in range(len(frames[i])):
            for x in range(len(frames[i][y])):
                hash_val = poseidon(hash_val,frames[i][y][x])
        frames_hash_values.append(hash_val)
    return frames_hash_values

def integrity_frames_hash(prev_hash_val, frame_data: list):
    hash_val = prev_hash_val
    for i in tqdm(range(len(frame_data))):
        hash_val = poseidon(hash_val,frame_data[i])
    return hash_val
    
def frame_hashes(frames: list):
    frames_hash_values = []
    hash_val = "0x00"
    for i in tqdm(range(len(frames))):
        for y in range(len(frames[i])):
            hash_val = poseidon(hash_val,frames[i][y])
        frames_hash_values.append(hash_val)
    return frames_hash_values


if __name__ == "__main__":
    # Example usage
    num1 = 123456789
    num2 = 987654321
    result = poseidon(num1, num2)
    print(f"Result: {result}")
