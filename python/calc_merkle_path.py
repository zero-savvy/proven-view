import json

def read_merkle_tree(file_path):
    """Read the Merkle tree from a JSON file."""
    with open(file_path, 'r') as f:
        merkle_tree = json.load(f)
    return merkle_tree

def get_merkle_path(merkle_tree, leaf_index):
    """Get the Merkle path for a given leaf index."""
    path = []
    position = []
    num_levels = len(merkle_tree)
    
    # Traverse from the leaf to the root
    current_index = leaf_index
    for level in range(num_levels - 1):
        # Determine the index of the sibling
        sibling_index = current_index ^ 1
        sibling_value = merkle_tree[level][sibling_index]
        
        # Append the sibling value to the path
        path.append(sibling_value)
        position.append(int(sibling_index < current_index))
        
        # Move to the parent index
        current_index //= 2
    
    return path, position

def main():
    # Read the Merkle tree from the file
    merkle_tree = read_merkle_tree('tree.json')
    
    # Specify the leaf index for which to get the Merkle path
    leaf_index = 3  # Example index, change as needed
    
    # Get the Merkle path
    merkle_path = get_merkle_path(merkle_tree, leaf_index)
    
    print(f"Merkle Path for leaf index {leaf_index}: {merkle_path}")

if __name__ == "__main__":
    main()
