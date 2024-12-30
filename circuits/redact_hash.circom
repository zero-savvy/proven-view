pragma circom 2.0.0;

include "utils/array_hasher.circom";


template RedactStep(n){
    // public inputs
    signal input step_in[2];
    
    // private inputs
    signal input data [n];
    signal input redact [n];
    
    //outputs
    signal output step_out[2];
    
    // Decode input Signals
    var prev_orig_hash = step_in[0];
    var prev_redact_hash = step_in[1];

    component hasher = ArrayHasher(n+1);
    component hasher_redact = ArrayHasher(n+1);
    hasher.data[0] <== prev_orig_hash;
    hasher_redact.data[0] <== prev_redact_hash;
    // hasher.data[1..n+1] <== data;
    for (var i = 1 ; i < n+1; i++) {
        redact[i-1]* (redact[i-1] - 1) === 0;
        hasher_redact.data[i] <== data[i-1] * redact[i-1];

        hasher.data[i] <== data[i-1];
    } 

    step_out[0] <== hasher.hash;  // originl_hash
    step_out[1] <== hasher_redact.hash;  // redact_hash
}

component main { public [step_in] } = RedactStep(10);