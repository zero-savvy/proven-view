include "node_modules/circomlib/circuits/bitify.circom";
include "node_modules/circomlib/circuits/poseidon.circom";
include "tornado-core/circuits/merkleTree.circom";

// Prove being a member of a valid Merkle tree
template Attest(levels) {
    signal input root;
    signal input firstFrameHash;
    signal input lastFrameHash;
    signal input firstPathElements[levels];
    signal input firstPathIndices[levels];
    signal input lastPathElements[levels];
    signal input lastPathIndices[levels];
    
    // No need to check leaf === hashValue
    // This constraint will be passed if-and-only-if the hashValue
    // actually belongs to the Merkle tree of the given root,
    // which is checked in MerkleTreeChecker component :)
    component firstTree = MerkleTreeChecker(levels);
    firstTree.leaf <== firstFrameHash;
    firstTree.root <== root;
    for (var i = 0; i < levels; i++) {
        FirstTree.pathElements[i] <== firstPathElements[i];
        FirstTree.pathIndices[i] <== firstPathIndices[i];
    }

    component lastTree = MerkleTreeChecker(levels);
    lastTree.leaf <== lastFrameHash;
    lastTree.root <== root;
    for (var i = 0; i < levels; i++) {
        lastTree.pathElements[i] <== lastPathElements[i];
        lastTree.pathIndices[i] <== lastPathIndices[i];
    }
}

component main {public [root, firstFrameHash, lastFrameHash]} = Attest(10);