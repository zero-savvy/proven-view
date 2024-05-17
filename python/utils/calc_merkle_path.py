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
    for level in reversed(merkle_tree[1:]):
        # Determine the index of the sibling
        sibling_index = current_index ^ 1
        sibling_value = level[sibling_index]
        
        # Append the sibling value to the path
        path.append(sibling_value)
        position.append(int(sibling_index < current_index))
        
        # Move to the parent index
        current_index //= 2
    
    return path, position

def get_merkle_path(leaf_index: int, tree_path):
    # Read the Merkle tree from the file
    merkle_tree = read_merkle_tree(tree_path)
    
    # Get the Merkle path
    merkle_path, positions = get_merkle_path(merkle_tree, leaf_index)
    
    print(f"Merkle Path for leaf index {leaf_index}: {merkle_path}, {positions}")


if __name__ == "__main__":
    get_merkle_path(3, 'tree.json')
