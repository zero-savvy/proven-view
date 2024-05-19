pragma circom 2.0.0;

include "node_modules/circomlib/circuits/bitify.circom";
include "node_modules/circomlib/circuits/poseidon.circom";


// template DoubleShiftRight() {
//     signal input in;
//     signal output out;
    
//     component toBits = Num2Bits(8);
// 	component toNum = Bits2Num(6);

//     toBits.in <== in;
//     toNum.in[0] <== toBits.out[2];
//     toNum.in[1] <== toBits.out[3];
//     toNum.in[2] <== toBits.out[4];
//     toNum.in[3] <== toBits.out[5];
//     toNum.in[4] <== toBits.out[6];
//     toNum.in[5] <== toBits.out[7];

//     out <== toNum.out;

// }

// template Resize(width, height){
//     signal input in[height][width];
//     var new_height = height/2;
//     var new_width = width/2;
//     signal output out[new_height][new_width];

//     component divider[height][width];

//     for(var i = 0; i < new_height; i++){
//         for(var j=0; j< new_width; j++){
//             divider[i*2][j*2] = DoubleShiftRight();
//             divider[i*2][j*2].in <== in[i*2][j*2];
//             divider[i*2][j*2+1] = DoubleShiftRight();
//             divider[i*2][j*2+1].in <== in[i*2][j*2+1];
//             divider[i*2+1][j*2] = DoubleShiftRight();
//             divider[i*2+1][j*2].in <== in[i*2+1][j*2];
//             divider[i*2+1][j*2+1] = DoubleShiftRight();
//             divider[i*2+1][j*2+1].in <== in[i*2+1][j*2+1];
            
//             var mean = divider[i*2][j*2].out + divider[i*2][j*2+1].out + divider[i*2+1][j*2].out + divider[i*2+1][j*2+1].out;
//             // var mean = (in[i*2][j*2] + in[i*2][j*2+1] + in[i*2+1][j*2] + in[i*2+1][j*2+1]) \ 4;
//             log(mean);
//             out[i][j] <== mean;
//         }
//     }

// }


template ResizeNearest(width, height){
    signal input in[height][width];
    var new_height = height/2;
    var new_width = width/2;
    signal output out[new_height][new_width];

    for(var i = 0; i < new_height; i++){
        for(var j=0; j< new_width; j++){
            out[i][j] <== in[i*2][j*2];
            if (in[i*2][j*2] > 255) {
                log(in[i*2][j*2]);
            }
        }
    }

}

template CompressorGray(size){
    signal input in[size];
	signal output out;

	component toBits[size];
	component toNum = Bits2Num(size * 8);

	for (var i=0; i<size; i++) {
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

    // public inputs
    signal input step_in;

    // signal output hash_out;
    signal input compressed [40];

    //outputs
    signal output step_out;

    signal prev_hash <== step_in;

    // component resize1 = ResizeNearest(640, 480);
    // resize1.in <== gray_input;
    
    // component resize2 = ResizeNearest(320, 240);
    // resize2.in <== resize1.out;

    // component resize3 = ResizeNearest(160, 120);
    // resize3.in <== resize2.out;

    // component resize4 = ResizeNearest(80, 60);
    // resize4.in <== resize3.out;

    // component compressor[40];
    // for (var i=0; i < 40; i++) {
    //     compressor[i] = CompressorGray(30);
    //     for (var j=0; j < 30; j++) { 
    //         compressor[i].in[j] <== resize4.out[j][i];
    //     }
    // }
    
    component hasher[39];

    for(var i=0; i < 39; i++) {
        hasher[i] = Poseidon(2);
        hasher[i].inputs[0] <== i == 0 ? compressed[0] : hasher[i-1].out;
        hasher[i].inputs[1] <== compressed[i+1];
    }
    
    component final_hash = Poseidon(2);
    final_hash.inputs[0] <== prev_hash;
    final_hash.inputs[1] <== hasher[38].out;
    step_out <== final_hash.out;
    // log(step_out);

}


component main {public [step_in]}  = GrayScaleHash(640, 480);



