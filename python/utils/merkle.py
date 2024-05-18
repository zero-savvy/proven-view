import json
import math
from utils.poseidon import poseidon


def pad_to_power_of_two(data):
    """Pad the list with zeros until its length is a power of two."""
    length = len(data)
    next_power_of_two = 2**math.ceil(math.log2(length))
    return data + ["0x00"] * (next_power_of_two - length)

def build_merkle_tree(data):
    """Build a Merkle tree from the data list using the Poseidon hash function."""
    # Pad data to the next power of two
    padded_data = pad_to_power_of_two(data)
    
    # Initialize the list of tree levels, starting with the leaf nodes
    tree = [padded_data]
    
    # Construct the tree from the bottom up
    while len(tree[0]) > 1:
        current_level = tree[0]
        next_level = []
        
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1]
            next_level.append(poseidon(left, right))
        
        tree.insert(0, next_level)
    
    return tree

def main():
    # Read the input list of numbers from the JSON file
    with open('outputs.json', 'r') as f:
        data = json.load(f)
    
    # Get the Merkle root
    tree = build_merkle_tree(data)

    with open('tree.json', 'w') as f:
        json.dump(tree, f, indent=4)
    
    
    print(f"Merkle Root: {tree[0][0]}")

if __name__ == "__main__":
    main()
