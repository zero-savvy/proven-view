pragma circom 2.0.0;

include "utils/row_hasher.circom";


template HashImg(widthOrig, nRows){
    // public inputs
    signal input step_in;
    
    // private inputs
    signal input row_orig [nRows][widthOrig];
    
    //outputs
    signal output step_out;
    
    // Decode input Signals
    var prev_orig_hash = step_in;

    // encoding signals
    var next_orig_hash;
    var next_crop_hash;

    component orig_row_hasher [nRows];
    component orig_hasher [nRows];
    
    for (var i = 0 ; i < nRows; i++) {
        orig_row_hasher[i] = RowHasher(widthOrig);
        orig_hasher[i] = Hasher(2);

        orig_row_hasher[i].img <== row_orig[i];
        orig_hasher[i].values[0] <== i == 0? prev_orig_hash : orig_hasher[i-1].hash;
        orig_hasher[i].values[1] <== orig_row_hasher[i].hash;
    } 
    

    step_out <== orig_hasher[nRows-1].hash;    
}

component main { public [step_in] } = HashImg(128, 10);