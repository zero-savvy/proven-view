pragma circom 2.0.0;

include "utils/array_hasher.circom";


template OneHashStep(){
    // public inputs
    signal input step_in;
    
    // private inputs
    signal input data;
    
    //outputs
    signal output step_out;
    
    // Decode input Signals
    var prev_orig_hash = step_in;

    component hasher = Hasher(2);
    hasher.values[0] <== step_in;
    hasher.values[1] <== data;
    step_out <== hasher.hash;    
}

component main { public [step_in] } = OneHashStep();