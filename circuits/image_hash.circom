pragma circom 2.0.0;

include "node_modules/circomlib/circuits/bitify.circom";
include "node_modules/circomlib/circuits/poseidon.circom";


template GrayScale(n) {
    signal input in[n][3];
    // signal input gray[n];

    signal output out[n];
    // signal output n_check;
 
    component lt[n][2];

    for (var i = 0; i < n; i++) {      
        var gray_value = 299 * in[i][0] + 587 * in[i][1] + 114 * in[i][2];
        out[i] <== gray_value;
    }
}

template Resize(width, height){
    signal input in[height][width];
    var new_height = height/2;
    var new_width = width/2;
    signal output out[new_height][new_width];


    for(var i = 0; i < new_height; i++){
        for(var j=0; j< new_width; j++){
            var mean = (in[i][j*2] + in[i][j*2+1] + in[i+1][j*2] + in[i+1][j*2+1])/4;
            out[i][j] <== mean;
        }
    }

}

template CompressorGrey(size){
    signal input in[size];
	signal output out;

	component toBits[size];
	component toNum = Bits2Num(size * 8);

	for (var i=0; i<size; i++) {
		var j=0;
        toBits[i] = Num2Bits(8);
        toBits[i].in <== in[i];
		toNum.in[i*8] <== toBits[i].out[0];
		toNum.in[i*8+1] <== toBits[i].out[1];
		toNum.in[i*8+2] <== toBits[i].out[2];
		toNum.in[i*8+3] <== toBits[i].out[3];
		toNum.in[i*8+4] <== toBits[i].out[4];
		toNum.in[i*8+5] <== toBits[i].out[5];
		toNum.in[i*8+6] <== toBits[i].out[6];
		toNum.in[i*8+7] <== toBits[i].out[7];
	}

	out <== toNum.out;
}


template GrayScaleHash(width, height){

    signal input orig[height][width][3];
    signal output hash_out;
    signal gray_input [height][width];

    // grayscale code here ...
    component grayscale[height];

    for (var i = 0; i< height; i++){
        grayscale[i] = GrayScale(width);
        grayscale[i].in <== orig[i];
        gray_input[i] <== grayscale[i].out;
    }

    component resize1 = Resize(640, 480);
    resize1.in <== gray_input;
    
    component resize2 = Resize(320, 240);
    resize2.in <== resize1.out;

    component resize3 = Resize(160, 120);
    resize3.in <== resize2.out;

    component resize4 = Resize(80, 60);
    resize4.in <== resize3.out;

    // component resize5 = Resize(40, 30);
    // resize5.in <== resize4.out;

    component compressor[40];
    for (var i=0; i < 40; i++) {
        compressor[i] = CompressorGrey(30);
        for (var j=0; j < 30; j++) { 
            compressor[i].in[j] <== resize4.out[j][i];
        }

    }
    
    component hasher[39];

    for(var i=0; i < 39; i++) {
    hasher[i] = Poseidon(2);
    hasher[i].inputs[0] <== i == 0 ? compressor[0].out : hasher[i-1].out;
    hasher[i].inputs[1] <== compressor[i+1].out;
    }

    hash_out <== hasher[38].out;
}


component main = GrayScaleHash(640, 480);



