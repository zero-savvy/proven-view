pragma circom 2.0.0;
include "../node_modules/circomlib/circuits/poseidon.circom";

template Hasher(inputSize) {
    signal input values[inputSize];
    signal output hash;

    component hasher = Poseidon(inputSize);
    for (var i = 0; i < inputSize; i++) {
        hasher.inputs[i] <== values[i];
    }
    hash <== hasher.out;
}


template ArrayHasher (size) {
    signal input data[size];
    signal output hash;

    component hasher[size-1];

    for(var i=0; i < size-1; i++) {
        hasher[i] = Hasher(2);
        hasher[i].values[0] <== i == 0 ? data[0] : hasher[i-1].hash;
        hasher[i].values[1] <== data[i+1];
    }

    hash <== hasher[size-2].hash;

}