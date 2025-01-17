include "node_modules/circomlib/circuits/bitify.circom";
include "node_modules/circomlib/circuits/poseidon.circom";


// if s == 0 returns [in[0], in[1]]
// if s == 1 returns [in[1], in[0]]
template DualMux() {
    signal input in[2];
    signal input s;
    signal output out[2];

    s * (1 - s) === 0;
    out[0] <== (in[1] - in[0])*s + in[0];
    out[1] <== (in[0] - in[1])*s + in[1];
}

// Prove being a member of a valid Merkle tree
template MerkleHash() {
    signal input step_in[2];
    signal output step_out[2];

    signal input firstPathElement;
    signal input firstPathSel;
    signal input lastPathElement;
    signal input lastPathSel;
    
    component firstHash = Poseidon(2);
    component firstDual = DualMux();
    firstDual.in[0] <== step_in[0];
    firstDual.in[1] <== firstPathElement;
    firstDual.s <== firstPathSel;
    firstHash.inputs <== firstDual.out;
    step_out[0] <== firstHash.out;

    component lastHash = Poseidon(2);
    component lastDual = DualMux();
    lastDual.in[0] <== step_in[1];
    lastDual.in[1] <== lastPathElement;
    lastDual.s <== lastPathSel;
    lastHash.inputs <== lastDual.out;
    step_out[1] <== lastHash.out;

    log(step_in[0]);
    log(step_in[1]);
}

component main {public [step_in]} = MerkleHash();