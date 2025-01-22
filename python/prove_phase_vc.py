# This code converts video file to its frames and save the selected range of them (start-end).
import os
import json

from utils.calc_merkle_path import prep_folding_input


if __name__ == "__main__":
    sub_tree_size = int(input("Enter sub tree size: ") or "64")
    output_path = "output"

    # Create inputs for Nova prover
    merkle_file = output_path + '/Merkle_tree.json'
    folding_tree_input = prep_folding_input(merkle_file, sub_tree_size)
    with open(f"{output_path}/folding_tree_input.json", 'w') as fp:
        json.dump(folding_tree_input, fp, indent=4)
