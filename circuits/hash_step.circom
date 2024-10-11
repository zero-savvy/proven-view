pragma circom 2.0.0;

include "utils/array_hasher.circom";


template HashStep(n){
    // public inputs
    signal input step_in;
    
    // private inputs
    signal input data [n];
    
    //outputs
    signal output step_out;
    
    // Decode input Signals
    var prev_orig_hash = step_in;

    component hasher = ArrayHasher(n+1);
    hasher.data[0] <== step_in;
    // hasher.data[1..n+1] <== data;
    for (var i = 1 ; i < n+1; i++) {
        hasher.data[i] <== data[i-1];
    } 

    step_out <== hasher.hash;    
}

component main { public [step_in] } = HashStep(1);