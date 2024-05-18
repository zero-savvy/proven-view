def compress(array_in):
    
    output_array = []
    # print(len(array_in), len(array_in[0]), len(array_in[0][0]))
    for frame in array_in:
        frame_array = []
        for i in range(0, len(frame)):
            hexValue = ''
            for j in range(0, len(frame[i])):
                hexValue = hex(int(frame[i][j]))[2:].zfill(2) + hexValue
            frame_array.append("0x" + hexValue)
        output_array.append(frame_array)
    return output_array
