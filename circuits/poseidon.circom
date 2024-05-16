include "node_modules/circomlib/circuits/poseidon.circom";

template Hasher(){
    signal input in1;
    signal input in2;
	signal output out;

    component hasher = Poseidon(2);
    hasher.inputs[0] <== in1;
    hasher.inputs[1] <== in2;

    log(hasher.out);

    out <== hasher.out;

}

component main {public [in1, in2]}  = Hasher();