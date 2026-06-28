import json
import math
import random
import string
from utils.poseidon import poseidon


def generate_random_number(length=62):
    """Generate a random number string with the specified length."""
    # Use digits 0-9 for the random number
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))

def generate_random_numbers(count, length=62):
    """Generate a list of random number strings."""
    random_numbers = []
    for _ in range(count):
        # Format as hexadecimal string to match the expected format
        random_number = "0x" + generate_random_number(length)
        random_numbers.append(random_number)
    return random_numbers

def save_to_json(data, filename="random_input.json"):
    """Save the generated data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Successfully saved {len(data)} random numbers to {filename}")

def pad_to_power_of_two(data):
    """Pad the list with zeros until its length is a power of two."""
    length = len(data)
    next_power_of_two = 2**math.ceil(math.log2(length))
    return data + ["0x00"] * (next_power_of_two - length)

def create_chain_hash(data):
    """
    Transform the data list into a chain hash:
    [a0, a1, a2, ...] -> [H(0, a0), H(H(0, a0), a1), H(H(H(0, a0), a1), a2), ...]
    """
    if not data:
        return []
    
    chain_hashed_list = []
    # Start with H(0, a0)
    previous_hash = poseidon("0x00", data[0])
    chain_hashed_list.append(previous_hash)
    
    # Build the chain: H(previous_hash, current_element)
    for i in range(1, len(data)):
        current_hash = poseidon(previous_hash, data[i])
        chain_hashed_list.append(current_hash)
        previous_hash = current_hash
    
    return chain_hashed_list

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

def build_chain_hash_merkle_tree(data):
    """
    First create a chain hash of the data list, then build a Merkle tree based on the chain hash.
    """
    # Create the chain hash
    chain_hashed_list = create_chain_hash(data)
    
    # Build the Merkle tree using the chain hashed list
    return build_merkle_tree(chain_hashed_list)

def main():
    # Read the input list of numbers from the JSON file
    # with open('outputs.json', 'r') as f:
    #     data = json.load(f)

    count = 1024
    random_numbers = generate_random_numbers(count, 20)
    
    # Save to JSON file
    save_to_json(random_numbers)
    
    # Print a sample of the generated numbers
    print("Sample of generated numbers:")
    for i, num in enumerate(random_numbers[:3]):  # Show first 3 numbers
        print(f"{i+1}: {num}")
    
    # Get the Merkle tree with chain hashing
    tree = build_chain_hash_merkle_tree(random_numbers)
    
    with open('tree.json', 'w') as f:
        json.dump(tree, f, indent=4)
    
    print(f"Merkle Root: {tree[0][0]}")

if __name__ == "__main__":
    main()