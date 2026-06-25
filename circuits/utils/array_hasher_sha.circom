pragma circom 2.0.0;
include "circomlib/circuits/sha256/constants.circom";
include "circomlib/circuits/sha256/sha256compression.circom";
include "circomlib/circuits/bitify.circom";

template Sha256_2() {
    signal input a;
    signal input b;
    signal output out;

    var i;
    var k;

    component bits2num = Bits2Num(216);
    component num2bits[2];

    num2bits[0] = Num2Bits(216);
    num2bits[1] = Num2Bits(216);

    num2bits[0].in <== a;
    num2bits[1].in <== b;


    component sha256compression = Sha256compression() ;

    component ha0 = H(0);
    component hb0 = H(1);
    component hc0 = H(2);
    component hd0 = H(3);
    component he0 = H(4);
    component hf0 = H(5);
    component hg0 = H(6);
    component hh0 = H(7);

    for (k=0; k<32; k++ ) {
        sha256compression.hin[0*32+k] <== ha0.out[k];
        sha256compression.hin[1*32+k] <== hb0.out[k];
        sha256compression.hin[2*32+k] <== hc0.out[k];
        sha256compression.hin[3*32+k] <== hd0.out[k];
        sha256compression.hin[4*32+k] <== he0.out[k];
        sha256compression.hin[5*32+k] <== hf0.out[k];
        sha256compression.hin[6*32+k] <== hg0.out[k];
        sha256compression.hin[7*32+k] <== hh0.out[k];
    }

    for (i=0; i<216; i++) {
        sha256compression.inp[i] <== num2bits[0].out[215-i];
        sha256compression.inp[i+216] <== num2bits[1].out[215-i];
    }

    sha256compression.inp[432] <== 1;

    for (i=433; i<503; i++) {
        sha256compression.inp[i] <== 0;
    }

    sha256compression.inp[503] <== 1;
    sha256compression.inp[504] <== 1;
    sha256compression.inp[505] <== 0;
    sha256compression.inp[506] <== 1;
    sha256compression.inp[507] <== 1;
    sha256compression.inp[508] <== 0;
    sha256compression.inp[509] <== 0;
    sha256compression.inp[510] <== 0;
    sha256compression.inp[511] <== 0;

    for (i=0; i<216; i++) {
        bits2num.in[i] <== sha256compression.out[255-i];
    }

    out <== bits2num.out;
}

template Sha256_2_bin() {
    signal input a[216];
    signal input b[216];
    signal output out[256];

    var i;
    var k;

    // component bits2num = Bits2Num(216);
    // component num2bits[2];

    // num2bits[0] = Num2Bits(216);
    // num2bits[1] = Num2Bits(216);

    // num2bits[0].in <== a;
    // num2bits[1].in <== b;


    component sha256compression = Sha256compression() ;

    component ha0 = H(0);
    component hb0 = H(1);
    component hc0 = H(2);
    component hd0 = H(3);
    component he0 = H(4);
    component hf0 = H(5);
    component hg0 = H(6);
    component hh0 = H(7);

    for (k=0; k<32; k++ ) {
        sha256compression.hin[0*32+k] <== ha0.out[k];
        sha256compression.hin[1*32+k] <== hb0.out[k];
        sha256compression.hin[2*32+k] <== hc0.out[k];
        sha256compression.hin[3*32+k] <== hd0.out[k];
        sha256compression.hin[4*32+k] <== he0.out[k];
        sha256compression.hin[5*32+k] <== hf0.out[k];
        sha256compression.hin[6*32+k] <== hg0.out[k];
        sha256compression.hin[7*32+k] <== hh0.out[k];
    }

    for (i=0; i<216; i++) {
        sha256compression.inp[i] <== a[215-i];
        sha256compression.inp[i+216] <== b[215-i];
    }

    sha256compression.inp[432] <== 1;

    for (i=433; i<503; i++) {
        sha256compression.inp[i] <== 0;
    }

    sha256compression.inp[503] <== 1;
    sha256compression.inp[504] <== 1;
    sha256compression.inp[505] <== 0;
    sha256compression.inp[506] <== 1;
    sha256compression.inp[507] <== 1;
    sha256compression.inp[508] <== 0;
    sha256compression.inp[509] <== 0;
    sha256compression.inp[510] <== 0;
    sha256compression.inp[511] <== 0;

    // for (i=0; i<216; i++) {
    //     bits2num.in[i] <== sha256compression.out[255-i];
    // }

    out <== sha256compression.out;

    // out <== bits2num.out;
}



template ShaArrayHasher_opt (size) {
    signal input data[size];
    signal output hash;

    component hasher[size-1];
    component bits2num = Bits2Num(216);
    component num2bits[size];

    num2bits[0] = Num2Bits(216);
    num2bits[0].in <== data[0];
    num2bits[1] = Num2Bits(216);
    num2bits[1].in <== data[1];
    hasher[0] = Sha256_2_bin();
    hasher[0].a <== num2bits[0].out;
    hasher[0].b <== num2bits[1].out;

    for(var i=1; i < size-1; i++) {
        num2bits[i+1] = Num2Bits(216);
        num2bits[i+1].in <== data[i+1];
        hasher[i] = Sha256_2_bin();
        for (var j=0; j<216; j++) {
            hasher[i].a[j] <== hasher[i-1].out[255-j];
        }
        hasher[i].b <== num2bits[i+1].out;
    }

    // hash <== hasher[size-2].out;

    for (var i=0; i<216; i++) {
        bits2num.in[i] <== hasher[size-2].out[255-i];
    }
    hash <== bits2num.out;
}


template ShaArrayHasher (size) {
    signal input data[size];
    signal output hash;

    component hasher[size-1];

    for(var i=0; i < size-1; i++) {
        hasher[i] = Sha256_2();
        hasher[i].a <== i == 0 ? data[0] : hasher[i-1].out;
        hasher[i].b <== data[i+1];
    }

    hash <== hasher[size-2].out;

}