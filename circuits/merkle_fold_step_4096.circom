pragma circom 2.0.0;

include "utils/array_hasher.circom";
include "utils/merkle_builder.circom";


template MerkleFoldStep(subTreeLevels, pathLength){
    // public inputs
    signal input step_in[2];
    
    // private inputs
    signal input data [2**subTreeLevels];
    signal input pathElements[pathLength];
    signal input pathIndices[pathLength];

    
    //outputs
    signal output step_out[2];
    
    // Decode input Signals
    var root = step_in[0];
    var prevOrigHash = step_in[1];

    // leaves hash
    component hasher = ArrayHasher(2**subTreeLevels+1);
    hasher.data[0] <== prevOrigHash;
    // hasher.data[1..n+1] <== data;
    for (var i = 1 ; i < 2**subTreeLevels + 1; i++) {
        hasher.data[i] <== data[i-1];
    } 

    // Create Sub-tree
    component MB = MerkleBuilder(subTreeLevels);
    MB.leaves <== data;

    // Merkle Check, assert
    component tree = MerkleTreeChecker(pathLength);
    tree.leaf <== MB.root;
    tree.root <== root;
    tree.pathElements <== pathElements;
    tree.pathIndices <== pathIndices;
    
    step_out[0] <== root;    
    step_out[1] <== hasher.hash;    
}

component main { public [step_in] } = MerkleFoldStep(12, 8);